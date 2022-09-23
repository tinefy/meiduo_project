from django.urls import re_path

from . import views

app_name = 'carts'

urlpatterns = [
    re_path(r'^carts/$', views.CartsView.as_view(), name='carts'),
    re_path(r'^carts/(?P<select_all>selectall)/$', views.CartsView.as_view(), name='carts_select_all'),
    # re_path(r'^carts/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.CartsView.as_view(), name='carts'),
]
