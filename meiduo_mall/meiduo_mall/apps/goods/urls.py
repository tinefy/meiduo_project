from django.urls import re_path

from . import views

app_name = 'goods'

urlpatterns = [
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),
    re_path(r'^list/(?P<category_id>\d+)/$', views.ListView.as_view(), name='list_no_page_num'),
    re_path(r'^list/hot/(?P<category_id>\d+)/$', views.ListHotGoodsView.as_view(), name='list_hot'),
    re_path(r'^detail/(?P<sku_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^visit/(?P<category_id>\d+)/$', views.VisitCountView.as_view(), name='visit'),
]
