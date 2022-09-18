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
    """
    商品选项相关的表结构

    MySQL root@(none):meiduo> select * from tb_spu where id=1;
    +----+----------------------------+----------------------------+--------------------------+-------
    | id | create_time                | update_time                | name                     | sales | comments | brand_id | category1_id | category2_id | category3_id | desc_detail | desc_pack | desc_service |
    +----+----------------------------+----------------------------+--------------------------+-------
    | 1  | 2018-04-11 16:01:28.547507 | 2018-04-25 12:09:42.593672 | Apple MacBook Pro 笔记本 | 1     | 1        | 1        | 4            | 45           | 157          | 描述 | 包装 | 服务 |
    +----+----------------------------+----------------------------+--------------------------+-------

    MySQL root@(none):meiduo> select * from tb_sku where spu_id=1;
    +-------------+-------------+--------+-----------------------------------------------------+
    | id | create_time | update_time | name | caption | price    | cost_price | market_price | stock | sales | comments | is_launched | category_id | spu_id | default_image |
    +-------------+-------------+--------+-----------------------------------------------------+
    | 1  | 2018-04-11 17:28:21.804713 | 2018-04-25 11:09:04.532866 | Apple MacBook Pro 13.3英寸笔记本 银色   | 【全新2017款】MacBook Pro,一身才华，一触，即发 了解【黑五返场特惠】 更多产品请点击【美多官方Apple旗舰店】 | 11388.00 | 10350.00   | 13388.00     | 5     | 5     | 1        | 1           | 157         | 1      | group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429 |
    | 2  | 2018-04-12 06:53:54.575306 | 2018-04-23 11:44:03.825103 | Apple MacBook Pro 13.3英寸笔记本 深灰色 | 【全新2017款】MacBook Pro,一身才华，一触，即发 了解【黑五返场特惠】 更多产品请点击【美多官方Apple旗舰店】 | 11398.00 | 10388.00   | 13398.00     | 0     | 1     | 0        | 1           | 157         | 1      | group1/M00/00/02/CtM3BVrPCAOAIKRBAAGvaeRBMfc0463515 |
    +-------------+-------------+--------+-----------------------------------------------------+

    MySQL root@(none):meiduo> select * from tb_spu_specification where spu_id=1;
    +----+----------------------------+----------------------------+----------+--------+
    | id | create_time                | update_time                | name     | spu_id |
    +----+----------------------------+----------------------------+----------+--------+
    | 1  | 2018-04-11 17:20:30.142577 | 2018-04-11 17:20:30.142657 | 屏幕尺寸 | 1      |
    | 2  | 2018-04-11 17:21:57.862419 | 2018-04-11 17:21:57.862464 | 颜色     | 1      |
    | 3  | 2018-04-11 17:22:04.687913 | 2018-04-11 17:22:04.687956 | 版本     | 1      |
    +----+----------------------------+----------------------------+----------+--------+

    MySQL root@(none):meiduo> select * from tb_sku_specification where sku_id=1;
    +----+----------------------------+----------------------------+-----------+--------+---------+
    | id | create_time                | update_time                | option_id | sku_id | spec_id |
    +----+----------------------------+----------------------------+-----------+--------+---------+
    | 1  | 2018-04-11 17:53:37.178101 | 2018-04-11 17:53:37.178148 | 1         | 1      | 1       |
    | 2  | 2018-04-11 17:56:00.141036 | 2018-04-11 17:56:00.141078 | 4         | 1      | 2       |
    | 3  | 2018-04-11 17:56:17.907973 | 2018-04-11 17:56:17.908017 | 7         | 1      | 3       |
    +----+----------------------------+----------------------------+-----------+--------+---------+

    MySQL root@(none):meiduo> select * from tb_specification_option where spec_id in (1, 2, 3);
    +----+----------------------------+----------------------------+-------------------------+---------+
    | id | create_time                | update_time                | value                   | spec_id |
    +----+----------------------------+----------------------------+-------------------------+---------+
    | 1  | 2018-04-11 17:22:55.126053 | 2018-04-11 17:22:55.126095 | 13.3英寸                | 1       |
    | 2  | 2018-04-11 17:24:04.841221 | 2018-04-11 17:24:04.841265 | 15.4英寸                | 1       |
    | 3  | 2018-04-11 17:24:23.862341 | 2018-04-11 17:24:23.862385 | 深灰色                  | 2       |
    | 4  | 2018-04-11 17:24:35.256820 | 2018-04-11 17:24:35.256868 | 银色                    | 2       |
    | 5  | 2018-04-11 17:25:04.607535 | 2018-04-11 17:25:04.607604 | core i5/8G内存/256G存储 | 3       |
    | 6  | 2018-04-11 17:25:15.969671 | 2018-04-11 17:25:15.969714 | core i5/8G内存/128G存储 | 3       |
    | 7  | 2018-04-11 17:25:35.025857 | 2018-04-12 07:12:08.090494 | core i5/8G内存/512G存储 | 3       |
    +----+----------------------------+----------------------------+-------------------------+---------+
    """

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

        # 当前商品的所有sku_spec按spu_spec排序
        sku_skuspecs = sku.skuspecification_set.order_by('spec_id')
        # 当前商品的sku规格选项id列表,index为spu_spec的顺序
        sku_skuspec_option_ids_list = []
        for sku_skuspec in sku_skuspecs:
            sku_skuspec_option_ids_list.append(sku_skuspec.option.id)  # SpecificationOption

        # 获取当前商品同一spu下的的所有sku
        all_skus = sku.spu.sku_set.all()
        # 字典，每一个sku_id(value)对应所有sku_spec选项信息的id(key) {(1, 4, 7): 1, (1, 3, 7): 2}
        dict_k_skuspec_option_ids_v_sku_id = {}
        for every_sku in all_skus:
            # 每一个SKU的所有规格
            every_sku_skuspecs = every_sku.skuspecification_set.order_by('spec_id')
            # 每一个SKU的规格选项键，列表的每一项为规格选项信息的id
            every_sku_skuspecs_option_ids_list = []
            for every_sku_skuspec in every_sku_skuspecs:
                every_sku_skuspecs_option_ids_list.append(every_sku_skuspec.option.id)
            # key:每一个SKU的所有规格选项信息的id value:每一个SKU的id
            dict_k_skuspec_option_ids_v_sku_id[tuple(every_sku_skuspecs_option_ids_list)] = every_sku.id

        # 当前商品spu的规格
        spu_spuspecs = sku.spu.spuspecification_set.order_by('id')
        # 若当前sku的规格选项少于spu规格，则某些spu规格无选项，信息不全
        if len(sku_skuspec_option_ids_list) < len(spu_spuspecs):
            return HttpResponseNotFound('当前商品sku的规格选项不完整')
        # index为spu_specs的顺序，与sku_skuspec_option_ids_list的index一致
        for index, every_spuspec in enumerate(spu_spuspecs):
            # 当前商品的sku规格选项id列表 key = sku_spec_key.copy()
            key = sku_skuspec_option_ids_list[:]
            # 每一spu_spec的所有选项值
            every_spuspec_options = every_spuspec.specificationoption_set.all()
            #  每一spu_spec的所有选项中的每一个选项值
            for every_spuspec_option in every_spuspec_options:
                # 每一个选项值的id, 赋值给当前商品的sku规格选项id列表中，每一spu_spec的index所对应的值
                key[index] = every_spuspec_option.id
                # dict.get(a) a不存在时返回None,dict[a] a不存在时报错
                # 在字典中查询新的sku规格选项id列
                # 若存在，则返回sku_id，若不存在，则返回None
                # 给每一spu_spec的所有选项值中的每一个选项值对象新建的属性sku_id_added_attr
                # 这样每一个选项值，都有一个属性sku_id_added_attr，属性值为sku_id的，表明是哪个sku_id商品拥有的选项值
                # 属性值为None的，没有商品拥有此选项值
                every_spuspec_option.sku_id_added_attr = dict_k_skuspec_option_ids_v_sku_id.get(tuple(key))
            # 每一spu_spec的所有选项值，赋值给每一spu_spec对象新建的属性spuspec_options_added_attr
            # 每一spu_spec的所有选项值中的每一选项值都有属性sku_id_added_attr，表明是哪个sku_id商品拥有的选项值
            every_spuspec.spuspec_options_added_attr = every_spuspec_options

        context = {
            'categories': categories,  # 频道分类
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sku': sku,
            'specs': spu_spuspecs,
        }
        return render(request, 'detail.html', context=context)
