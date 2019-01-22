from django.conf import settings
from django.urls import path, include, resolve, Resolver404,reverse
from django.shortcuts import redirect
from shop import urls as frontend_urls
from Accounts.models import Account , Shop ,Category , Product
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from storefront import views,urls

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self,request):
        path = request.get_full_path()
        domain = request.META['HTTP_HOST']
        pieces = domain.split('.')
        redirect_path = "http://{0}{1}".format(
                settings.DEFAULT_SITE_DOMAIN, path)
        try:
            shop_details = Shop.objects.get(subdomain=domain)
            request.shop_details = shop_details.id
            request.active = shop_details.is_activated
        except Shop.DoesNotExist:
            pass
            return 
        return 


    

