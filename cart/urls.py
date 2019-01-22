from django.urls import re_path ,path

from . import views

app_name = 'cart'

urlpatterns = [
    re_path(r'^$', views.cart_detail, name='cart_detail'),
    path('cart_api/',views.order_cart_detail, name='cart_api'),
    re_path(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    re_path(r'^remove/(?P<product_id>\d+)/$',  views.cart_remove,  name='cart_remove'),
]
