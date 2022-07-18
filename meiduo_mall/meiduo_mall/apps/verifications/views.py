import base64

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from verifications.captcha.captcha import captcha
from django_redis import get_redis_connection

from . import constants


class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex(f'img_{uuid}', constants.IMAGE_CODE_REDIS_EXPIRES, text)
        image_base64 = base64.b64encode(image).decode()
        json_ = {
            'image': image_base64,
            'text': text,
        }
        return JsonResponse(json_)
