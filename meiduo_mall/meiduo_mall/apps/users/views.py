import re
# from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.urls import reverse
from django.views import View

from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.apps.verifications.views import CheckSMSCodeView
from meiduo_mall.utils.github_oauth import OAuthGitHub

# from meiduo_mall.apps.users.utils import UsernameMobileAuthBackend

# Create your views here.

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code = request.POST.get('sms_code')
        allow = request.POST.get('allow')
        info_list = [username, password, password2, mobile, sms_code, allow]
        if not all(info_list):
            return HttpResponseForbidden('缺少必传参数！')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入5-20个字符的用户名！')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码！')
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致！')

        check_sms_code_result = CheckSMSCodeView().check_sms_code(mobile, sms_code)
        if check_sms_code_result == -1:
            return render(request, 'register.html', {'sms_code_error_message': '短信验证错误！'})
        elif check_sms_code_result == -2:
            return render(request, 'register.html', {'sms_code_error_message': '短信验证过期！'})

        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议！')
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except:
            return render(request, 'register.html', {'register_errmsg': '注册失败！'})
        else:
            login(request, user)
            response = redirect(reverse('contents:index'))
            response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
            return response


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        json_ = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        }
        return JsonResponse(json_)


class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        json_ = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        }
        return JsonResponse(json_)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        next_ = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        necessary_info_list = [username, password]
        if not all(necessary_info_list):
            return HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[\w\d_-]{5,20}$', username):
            return HttpResponseForbidden('请输入正确的用户名或手机号')
        if not re.match(r'^[\w\d]{8,20}$', password):
            return HttpResponseForbidden('密码最少8位，最长20位')
        # user = UsernameMobileAuthBackend().authenticate(username=username, password=password)
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
        login(request, user=user)
        if remembered != 'on':
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        if next_:
            response = redirect(next_)
        else:
            response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class GitHubOAuthURLView(View):
    def get(self, request):
        next_ = request.GET.get('next')
        github = OAuthGitHub(client_id='d8b3fafc3117d57cdeff', state=next_)
        url = github.get_github_url()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': url})


class GitHubOAuthView(View):
    def get(self, request):
        code = request.GET.get('code')
        next_ = request.GET.get('state')
        github = OAuthGitHub(client_id='d8b3fafc3117d57cdeff', client_secret='59814cab59d6d0a4a29f1c7c9942abc237337840',
                             code=code)
        github.get_github_access_token()
        github_user_info = github.get_github_user_info()
        github_user_info['netx'] = next_
        return HttpResponse(str(github_user_info))

    def post(self, request):
        pass


class UserInfoView(LoginRequiredMixin, View):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))
        return render(request, 'user_center_info.html')
