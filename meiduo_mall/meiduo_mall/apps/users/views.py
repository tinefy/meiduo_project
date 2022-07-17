import re
# from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login

# Create your views here.
from django.urls import reverse
from django.views import View

from meiduo_mall.utils.response_code import RETCODE

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        info_list = [username, password, password2, mobile, allow]
        if not all(info_list):
            return HttpResponseForbidden('缺少必传参数！')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入5-20个字符的用户名！')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码！')
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致！')
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议！')
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except:
            return render(request, 'register.html', {'register_errmsg': '注册失败！'})
        else:
            login(request, user)
            return redirect(reverse('contents:index'))


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        json_ = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        }
        return JsonResponse(json_)
