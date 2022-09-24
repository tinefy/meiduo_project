import base64
import pickle

from django_redis import get_redis_connection


def cart_merge(request, user, response):
    """登录后合并cookie购物车数据到Redis"""
    # 查询cookies购物车
    cookie_carts_str = request.COOKIES.get('carts')
    # 用户从没有操作过cookie购物车
    if not cookie_carts_str:
        return response

    # 如果用户操作过cookie购物车
    # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
    cookie_carts_dict = pickle.loads(base64.b64decode(cookie_carts_str.encode()))

    cookie_carts_dict_ = {}
    for key, value in cookie_carts_dict.items():
        cookie_carts_dict_[int(key)] = value
    cookie_carts_dict = cookie_carts_dict_

    # if user.is_authenticated:
    # 用户已登录，合并入redis购物车
    sku_ids = cookie_carts_dict.keys()
    redis_conn = get_redis_connection('carts')
    redis_pipeline = redis_conn.pipeline()
    for sku_id in sku_ids:
        redis_pipeline.hincrby(f'carts_{user.id}', sku_id, cookie_carts_dict[sku_id]['count'])
        if cookie_carts_dict[sku_id]['selected']:
            redis_pipeline.sadd(f'selected_{user.id}', sku_id)
        else:
            redis_pipeline.srem(f'selected_{user.id}', sku_id)
    redis_pipeline.execute()

    response.delete_cookie('carts')
    return response
