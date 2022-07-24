from django.urls import re_path
from . import views

app_name = 'users'

urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view(), name='usernames'),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view(), name='mobiles'),
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
