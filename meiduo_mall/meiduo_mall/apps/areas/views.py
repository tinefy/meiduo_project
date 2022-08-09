import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import Area
from meiduo_mall.utils.response_code import RETCODE

logger = logging.Logger('django')


class AreasView(View):
    def get(self, request):
        area_id = request.GET.get('area_id')
        if not area_id:
            try:
                province_model_list = Area.objects.filter(parent__isnull=True)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})
            else:
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})
                return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
        else:
            pass
