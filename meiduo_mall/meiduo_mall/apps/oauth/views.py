from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse

from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.github_oauth import OAuthGitHub
from meiduo_mall.apps.oauth.models import OAuthGitHubUser


# Create your views here.


class GitHubOAuthURLView(View):
    def get(self, request):
        next_ = request.GET.get('next')
        github = OAuthGitHub(client_id=settings.CLIENT_ID, state=next_)
        url = github.get_github_url()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': url})


class GitHubOAuthView(View):
    def get(self, request):
        code = request.GET.get('code')
        next_ = request.GET.get('state')
        github = OAuthGitHub(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET,
                             code=code)
        github.get_github_access_token()
        github_user_info = github.get_github_user_info()
        try:
            oauth_user = OAuthGitHubUser.objects.get(openid=github_user_info['id'])
        except OAuthGitHubUser.DoesNotExist:
            generate_access_token()
            context = {}
            return render(request, 'oauth_callback.html', context)
        else:
            github_user = oauth_user.user
            login(request, github_user)
            response = redirect(next_)
            response.set_cookie('username', github_user.username, max_age=3600 * 24 * 15)
        return response
