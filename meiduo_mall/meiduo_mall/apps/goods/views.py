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


class DetailView(View):
    def get(self, request, sku_id):
        # 获取当前sku的信息
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, '404.html')
        category = sku.category
        # 查询商品频道和分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 当前商品的所有规格 <QuerySet [<SKUSpecification: 1: Apple MacBook Pro 13.3英寸笔记本 银色: 屏幕尺寸 - 13.3英寸>, ...]>
        sku_specs = sku.skuspecification_set.order_by('spec_id')
        # 构建当前商品的规格选项键，列表的每一项为规格选项信息(例如 ”13.3英寸“)的id
        sku_specs_key = []
        for sku_spec in sku_specs:
            sku_specs_key.append(sku_spec.option.id)  # SpecificationOption

        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建所有sku字典，每一个sku id(value)对应所有的规格选项信息的id(key) spec_sku_map {(1, 4, 7): 1, (1, 3, 7): 2}
        spec_sku_map = {}
        for sku_item in skus:
            # 每一个SKU的所有规格
            sku_item_specs = sku_item.skuspecification_set.order_by('spec_id')
            # 每一个SKU的规格选项键，列表的每一项为规格选项信息的id
            sku_item_spec_key = []
            for sku_item_spec in sku_item_specs:
                sku_item_spec_key.append(sku_item_spec.option.id)
            # key:每一个SKU的所有规格选项信息的id value:每一个SKU的id
            spec_sku_map[tuple(sku_item_spec_key)] = sku_item.id

        # 获取当前商品的规格选项(例如 ”屏幕尺寸“) <QuerySet [<SPUSpecification: Apple MacBook Pro 笔记本: 屏幕尺寸>,...]>
        sku_spu_specs = sku.spu.spuspecification_set.order_by('id')
        # 若当前sku的规格选项少于spu规格选项，则信息不完整，则不再继续
        if len(sku_specs_key) < len(sku_spu_specs):
            return HttpResponseNotFound('当前商品sku的规格信息不完整')
        for index, sku_spu_spec in enumerate(sku_spu_specs):
            # key = sku_spec_key.copy()
            key = sku_specs_key[:]
            # 该规格选项的所有选项信息
            sku_spu_spec_options = sku_spu_spec.specificationoption_set.all()
            for sku_spu_spec_option in sku_spu_spec_options:
                key[index] = sku_spu_spec_option.id
                # dict.get(a) a不存在时返回None,dict[a] a不存在时报错
                sku_spu_spec_option.sku_id_added_attr = spec_sku_map.get(tuple(key))
            sku_spu_spec.spec_options_added_attr = sku_spu_spec_options

        context = {
            'categories': categories,  # 频道分类
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sku': sku,
            'spec': sku_spu_spec,
        }
        return render(request, 'detail.html', context=context)
