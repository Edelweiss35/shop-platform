from django.urls import re_path, path

from . import views

app_name = 'storefront'

urlpatterns = [
    path('shop-api/', views.product_list_api, name='product_list_api'),
    re_path(r'^$', views.product_list, name='product_list'),
    re_path(r'^(?P<category_slug>[-\w]+)/$',views.product_list, name='product_list_by_category'),
    re_path(r'^(?P<product_id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    ]
