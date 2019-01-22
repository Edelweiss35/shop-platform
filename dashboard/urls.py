from django.urls import path, include, re_path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('shop_withdraw/', views.shop_withdraw, name ='shop_withdraw'),
    path('refund/', views.refund_order, name ='refund'),
    path('update_product/', views.refund_order, name ='update_product'),
    path('delete_shop/', views.delete_shop, name ='delete_shop'),
    path('delete_products/', views.delete_products, name ='delete_products'),
    path('delete_category/', views.delete_category, name ='delete_category'),
    path('shop_settings/', views.shop_settings, name ='shop_settings'),
    path('createshop/', views.create_shop, name = 'createshop'),
    path('updateshop/', views.updateshop, name = 'updateshop'),
    path('product/', views.product_category, name = 'product'),
    path('shop-ui/', views.front_ui, name = 'shop-ui'),
    path('profile/', views.profile, name = 'profile')
]