import json

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU
from meiduo_mall.utils.response_code import RETCODE


# Create your views here.
class CartsView(View):
    """
    参数名 	类型 	是否必传 	说明
    sku_id 	int 	是 	商品SKU编号
    count 	int 	是 	商品数量
    selected 	bool 	否 	是否勾选
    """

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected')

        required = [sku_id, count]
        if not all(required):
            return HttpResponseForbidden('缺少必传参数')

        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return HttpResponseForbidden('商品不存在')
        try:
            count = int(count)
        except Exception:
            return HttpResponseForbidden('参数count有误')
        if not isinstance(selected, bool):
            return HttpResponseForbidden('参数selected有误')

        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            get_count_in_redis = redis_conn.hget(f'carts_{user.id}', sku_id)
            if (not get_count_in_redis and count >= 0) or (get_count_in_redis and (get_count_in_redis + count >= 0)):
                redis_pipeline = redis_conn.pipeline()
                redis_pipeline.hincrby(f'carts_{user.id}', sku_id, count)
                if selected:
                    redis_pipeline.sadd(f'selected_{user.id}', sku_id)
                redis_pipeline.execute()
            else:
                return JsonResponse({'code': RETCODE.OK, 'errmsg': '参数count有误'})
            return JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})
        else:
            # 用户未登录，操作cookie购物车
            pass
