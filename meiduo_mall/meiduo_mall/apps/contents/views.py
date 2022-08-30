from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import ContentCategory
from .utils import get_categories


class IndexView(View):

    def get(self, request):
        categories = get_categories()
        contents = {}
        content_categories = ContentCategory.objects.all()
        for category in content_categories:
            # contents的value是对象 {'index_lbt': <QuerySet [<Content: 轮播图: 美图M8s>, <Content: 轮播图: 黑色星期五>]>}
            contents[category.key] = category.content_set.filter(status=True).order_by('sequence')
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context=context)
