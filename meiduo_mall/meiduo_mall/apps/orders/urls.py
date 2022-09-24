from django.urls import re_path

from . import views

app_name = 'orders'

urlpatterns = [
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='orders_settlement'),
    # re_path(r'^carts/(?P<select_all>selectall)/$', views.CartsView.as_view(), name='carts_select_all'),
    # re_path(r'^carts/(?P<simple>simple)/$', views.CartsView.as_view(), name='carts_simple'),
]
