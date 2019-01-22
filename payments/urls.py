from django.conf.urls import url
from . import views
from django.urls import re_path, path

app_name = 'payments'

urlpatterns = [
    re_path(r'^process/$', views.payment_process, name='process'),
    re_path(r'^done/$', views.payment_done, name='done'),
    re_path(r'^canceled/$', views.payment_canceled, name='canceled'),
    path('mpesa/', views.mpesa_ecom_transaction , name = 'mpesa'),
    path('eazzypay/', views.eazzypay_ecom , name = 'eazzypay'),
    path('visa_mc/', views.visa_mc , name = 'visa_mc'),
    path('pay_on_delivery/', views.pay_on_delivery, name ='pay_on_delivery'),

]
