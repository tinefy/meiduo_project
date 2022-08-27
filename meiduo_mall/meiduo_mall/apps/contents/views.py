from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, request):
        categories = OrderedDict()
        print(type(categories))
        print(categories)
        return render(request, 'index.html')
