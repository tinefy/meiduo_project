from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from django_redis import get_redis_connection

from goods.models import SKU
from orders import constants
from users.models import Address


# Create your views here.
class OrderSettlementView(LoginRequiredMixin, View):
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
