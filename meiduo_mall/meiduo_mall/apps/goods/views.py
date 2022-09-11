from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

# Create your views here.
from contents.utils import get_categories

from .models import GoodsCategory
from .utils import get_breadcrumb


class ListView(View):
    def get(self, request, category_id, page_num):
        # def get(self, request):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return HttpResponseNotFound('GoodsCategory does not exist')
        # 查询商品频道和分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb()
        context = {
            'categories': categories,
            # 'contents': contents
        }
        # return render(request, 'list.html', context=context)
        return render(request, 'list.html', context=context)
