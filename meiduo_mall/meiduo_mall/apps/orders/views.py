import json
import logging
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.utils.timezone import localtime
from django.views import View

from django_redis import get_redis_connection

from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredJSONMixin

from goods.models import SKU
from users.models import Address

from . import constants
from .models import OrderInfo, OrderGoods

# Create your views here.
logger = logging.getLogger('django')


class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        user = request.user
        # 查询地址信息
        try:
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except Address.DoesNotExist:
            # 如果地址为空，渲染模板时会判断，并跳转到地址编辑页面
            addresses = None

        # 从Redis购物车中查询出被勾选的商品信息
        redis_conn = get_redis_connection('carts')
        carts_redis = redis_conn.hgetall(f'carts_{user.id}')
        selected_redis = redis_conn.smembers(f'selected_{user.id}')
        carts_dict = {}
        for sku_id in selected_redis:
            carts_dict[int(sku_id)] = int(carts_redis[sku_id])

        total_count = 0
        total_amount = Decimal(0.00)

        skus = SKU.objects.filter(id__in=carts_dict.keys())
        for sku in skus:
            sku.count = carts_dict[sku.id]
            sku.amount = sku.price * sku.count
            total_count += sku.count
            total_amount += sku.amount

        freight = Decimal(constants.FREIGHT_COST)

        context = {
            'user': user,
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight
        }
        return render(request, 'place_order.html', context=context)


class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')

        requirements = [address_id, pay_method]
        if not all(requirements):
            return HttpResponseForbidden('缺少必传参数')
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return HttpResponseForbidden('参数address_id错误')
        pay_methods = [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]
        if pay_method not in pay_methods:
            return HttpResponseForbidden('参数pay_method错误')

        user = request.user
        order_id = localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        with transaction.atomic():
            transaction_save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        'ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                # 从Redis购物车中查询出被勾选的商品信息
                redis_conn = get_redis_connection('carts')
                carts_redis = redis_conn.hgetall(f'carts_{user.id}')
                selected_redis = redis_conn.smembers(f'selected_{user.id}')
                carts_dict = {}
                for sku_id in selected_redis:
                    carts_dict[int(sku_id)] = int(carts_redis[sku_id])
                sku_ids = carts_dict.keys()

                for sku_id in sku_ids:
                    # 使用乐观锁
                    while True:
                        sku = SKU.objects.get(id=sku_id)

                        # 读取原始库存
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        sku_count = carts_dict[sku.id]
                        # 判断SKU库存
                        if sku_count > origin_stock:
                            # 库存不足，下单失败事务回滚，并中止执行
                            transaction.savepoint_rollback(transaction_save_id)
                            return JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                        # SKU减少库存，增加销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count

                        # update() returns the number of rows matched
                        # which may not be equal to the number of rows updated if some rows already have the new value
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        # 如果下单失败，但是库存足够时，继续下单，直到下单成功或者库存不足为止
                        if result == 0:
                            continue

                        # 修改SPU销量
                        sku.spu.sales += sku_count
                        sku.spu.save()

                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price,
                        )

                        order.total_count += sku_count
                        order.total_amount += (sku.price * sku_count)

                        # 下单成功跳出循环
                        break
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(transaction_save_id)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})
            else:
                transaction.savepoint_commit(transaction_save_id)

        redis_pipeline = redis_conn.pipeline()
        redis_pipeline.hdel(f'carts_{user.id}', *selected_redis)
        redis_pipeline.srem(f'selected_{user.id}', *selected_redis)
        redis_pipeline.execute()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})


class OrderSuccessView(LoginRequiredMixin, View):
    """提交订单成功"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context=context)
