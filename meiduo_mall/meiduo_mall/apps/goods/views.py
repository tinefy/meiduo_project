from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound, JsonResponse
from django.core.paginator import Paginator

# Create your views here.
from contents.utils import get_categories
from meiduo_mall.utils.response_code import RETCODE

from .models import GoodsCategory, SKU
from .utils import get_breadcrumb
from . import constants

''' http://127.0.0.1:8000/list/115/1/?sort=default '''


class ListView(View):
    def get(self, request, category_id, page_num):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return HttpResponseNotFound('GoodsCategory does not exist')
        # 接收sort参数：默认=default
        sort = request.GET.get('sort', 'default')
        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-sales'
        else:
            sort = 'default'
            sort_field = 'create_time'
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)
        # 创建分页器：每页N条记录
        paginator = Paginator(skus, constants.GOODS_LIST_LIMIT)
        # 获取列表页总页数
        total_page = paginator.num_pages
        # 获取当前页面sku数据
        if total_page >= int(page_num) >= 1:
            page_skus = paginator.page(page_num)
        else:
            return HttpResponseNotFound('page is empty')
        # 查询商品频道和分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)
        context = {
            'categories': categories,  # 频道分类
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sort': sort,  # 排序字段
            'category': category,
            'page_skus': page_skus,  # 当前页面sku数据
            'total_page': total_page,  # 总页数
            'page_num': page_num,  # 当前页码
        }
        return render(request, 'list.html', context=context)


class ListHotGoodsView(View):
    def get(self, request, category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'GoodsCategory does not exist'})
        hot_skus = []
        skus = SKU.objects.filter(category=category, is_launched=True).order_by('-sales')[:2]
        for sku in skus:
            sku_dict = {}
            sku_dict['id'] = sku.id
            sku_dict['default_image'] = sku.default_image
            sku_dict['name'] = sku.name
            sku_dict['price'] = sku.price
            hot_skus.append(sku_dict)
        print(hot_skus)
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})
