from django.urls import re_path

from . import views

app_name = 'contents'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^list/$', views.ListView.as_view(), name='list'),
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),
]
