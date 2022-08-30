from django.shortcuts import render
from django.views import View

# Create your views here.
from .utils import get_categories


class IndexView(View):

    def get(self, request):
        categories = get_categories()
        context = {
            'categories': categories
        }
        return render(request, 'index.html', context=context)
