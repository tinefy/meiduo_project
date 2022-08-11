import json
import logging
import re
# from django.contrib.auth.models import User
from multiprocessing import Process

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.urls import reverse
from django.views import View

from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.apps.verifications.views import CheckSMSCodeView
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from meiduo_mall.apps.users import constants
from .models import Address

# from meiduo_mall.apps.users.utils import UsernameMobileAuthBackend

# Create your views here.


User = get_user_model()

logger = logging.Logger('django')


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


class UserInfoView(LoginRequiredMixin, View):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context=context)


class UserEmailsView(LoginRequiredJSONMixin, View):
    def put(self, request):
        data = json.loads(request.body.decode())
        email = data['email']
        re_ = '^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'
        if not email:
            return HttpResponseForbidden('缺少email参数')
        if not re.match(re_, email):
            return HttpResponseForbidden('参数email有误')
        try:
            # request.user.email = email
            # request.user.save()
            User.objects.filter(username=request.user.username).update(email=email)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        def generate_email_verify_url(user):
            data_ = {'user_id': user.id, 'email': email}
            token = signing.dumps(data_)
            verify_url = settings.SITE_URL + reverse('users:emails_verification') + '?token=' + token
            return verify_url

        def send_mail_():
            verify_url = generate_email_verify_url(request.user)
            subject = "美多商城邮箱验证"
            html_message = '<p>尊敬的用户您好！</p>' \
                           '<p>感谢您使用美多商城。</p>' \
                           '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                           '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
            try:
                send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)
            except Exception as e:
                logger.error(e)

        send_mail_process = Process(target=send_mail_)
        send_mail_process.start()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class UserEmailsVerificationView(View):
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return HttpResponseBadRequest('缺少token')
        try:
            data_ = signing.loads(token, max_age=constants.EMAIL_VERIFICATION_CODE_EXPIRES)
        except Exception as e:
            logger.error(e)
            return HttpResponseForbidden('无效的token')
        try:
            User.objects.filter(id=data_['user_id'], email=data_['email']).update(email_active=True)
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError('激活邮件失败')
        return redirect(reverse('users:info'))


class UserAddressView(LoginRequiredMixin, View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user, is_deleted=False)
        '''
        等同于 addresses = Address.objects.filter(user_id=request.user.id, is_deleted=False)
        SQL Query:
        SELECT `tb_address`.`id`,
               `tb_address`.`create_time`,
               `tb_address`.`update_time`,
               `tb_address`.`user_id`,
               `tb_address`.`title`,
               `tb_address`.`receiver`,
               `tb_address`.`province_id`,
               `tb_address`.`city_id`,
               `tb_address`.`district_id`,
               `tb_address`.`place`,
               `tb_address`.`mobile`,
               `tb_address`.`tel`,
               `tb_address`.`email`,
               `tb_address`.`is_deleted`
        FROM `tb_address`
        WHERE (NOT `tb_address`.`is_deleted` AND `tb_address`.`user_id` = 21)
        ORDER BY `tb_address`.`update_time` DESC LIMIT 21
        '''
        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)
        context = {
            'default_address_id': request.user.default_address,
            'addresses': address_dict_list,
        }
        return render(request, 'user_center_site.html', context=context)


class UserAddressCreateView(LoginRequiredMixin, View):
    def post(self, request):
        return JsonResponse({})
