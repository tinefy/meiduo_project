import json
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
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
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,
            total_amount=Decimal('0'),
            freight=Decimal('10.00'),
            pay_method=pay_method,
            status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
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
            sku = SKU.objects.get(id=sku_id)
            sku_count = carts_dict[sku.id]
            # 判断SKU库存
            if sku_count > sku.stock:
                return JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})
            # SKU减少库存，增加销量
            sku.stock -= sku_count
            sku.sales += sku_count
            sku.save()
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
        order.total_amount += order.freight
        order.save()

        redis_pipeline = redis_conn.pipeline()
        redis_pipeline.hdel(f'carts_{user.id}', *selected_redis)
        redis_pipeline.srem(f'selected_{user.id}', *selected_redis)
        redis_pipeline.execute()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})
