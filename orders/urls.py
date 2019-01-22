from . import views
from django.urls import re_path, path



app_name = 'orders'

urlpatterns = [
        re_path(r'^create/$', views.order_create, name='order_create'),
        re_path(r'^delivery/$', views.delivery_method, name='delivery_method'),
        re_path(r'^review/$', views.order_review, name='order_review'),
        path('order_api/',views.order_review_api, name='order_api')
]