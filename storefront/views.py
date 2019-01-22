from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import json
from cart.forms import CartAddProductForm
from Accounts.models import Category, Product
from django.http import JsonResponse
from Accounts.models import Account, Shop , Product ,Category
from django.http import HttpResponse
from .forms import ChoiceForm
import json




def product_list(request, category_slug=None):
    value = getattr(request,'shop_details', None)
    active = getattr(request,'active', None)
    if request.user.is_authenticated:
        user =  request.user
        user_id = user.id
        account = Account.objects.get(User=user_id)
        account_id = account.id
        try:
            shop_name = Shop.objects.get(Account_id=account_id)
        except:
            return HttpResponse('there is no shop associated with this account')
    
        if category_slug:
            try:
                categories = Category.objects.filter(shop_name=shop_name.id, slug = category_slug)
            except:
                return HttpResponse("there are no product categories associated with your shop")
        else:
            try:
                categories = Category.objects.filter(shop_name=shop_name.id)
            except:
                return HttpResponse("there are no product categories associated with your shop")
        try:
            products = Product.objects.filter(category__in=categories).all()
        except:
            return HttpResponse("there are no product categories associated with your shop")
        shop_namez = shop_name.shop_name
        shop_logo = shop_name.shop_logo
        shop_phone = shop_name.phone_number
        shop_description = shop_name.shop_description
        shop_banner = shop_name.shop_banner
        if not shop_name:
            return HttpResponse('shop does not exists')
    elif value is not None:
        try:
            shop_names = Shop.objects.get(pk=request.shop_details)
        except:
            return HttpResponse('something wrong with getting the shop details')

        if category_slug:
            try:
                categories = Category.objects.filter(shop_name=request.shop_details, slug = category_slug)
            except:
                return HttpResponse("there are no product categories associated with your shop")
        else:
            try:
                categories = Category.objects.filter(shop_name=request.shop_details)
            except:
                return HttpResponse("there are no product categories associated with your shop")  

        try:
            products = Product.objects.filter(category__in=categories).all()
        except:
            return HttpResponse("there are no product categories associated with your shop")

        shop_namez = shop_names.shop_name
        shop_logo = shop_names.shop_logo
        shop_phone = shop_names.phone_number
        shop_description = shop_names.shop_description
        shop_banner =  shop_names.shop_banner

        if active == False:
            return render (request, 'list1-test.html', {'categories':  categories,'products':products, 
                'shop_banner':shop_banner, 'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone,'shop_description':shop_description })
        else:
            return render (request, 'shop/product/list1.html', {'categories':  categories,'products':products, 
                'shop_banner':shop_banner, 'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone,'shop_description':shop_description })
       
    else:
        return HttpResponse("please log in")
    if active == False:
        return render (request, 'list1-test.html', {'categories':  categories,'products':products, 
        'shop_banner':shop_banner, 'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone,'shop_description':shop_description })
    else:
        return render (request, 'shop/product/list1.html', {'categories':  categories,'products':products, 
        'shop_banner':shop_banner, 'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone,'shop_description':shop_description })




def product_list_api(request):
    
    value = getattr(request,'shop_details', None)

    if request.user.is_authenticated:
        user =  request.user
        user_id = user.id
        account = Account.objects.get(User=user_id)
        account_id = account.id
        shop_name = Shop.objects.get(Account_id=account_id)
        shop_banner = shop_name.shop_banner
        categories = Category.objects.filter(shop_name=shop_name.id)
        products = Product.objects.filter(category__in=categories).all()
        shop_namez = shop_name.shop_name
        shop_logo = shop_name.shop_logo
        shop_phone = shop_name.phone_number
        shop_description = shop_name. shop_description
        print('product list api')
        shop_data = json.dumps({'shop_name':shop_namez,'shop_phone':shop_phone, 'shop_description':shop_description})
        print('shop data', shop_data)
        return HttpResponse(shop_data)
    elif value is not None:
        try:
            shop_names = Shop.objects.get(pk=request.shop_details)
            shop_banner =  shop_names.shop_banner
            shop_namez = shop_names.shop_name
            shop_logo = shop_names.shop_logo
            shop_phone = shop_names.phone_number
            shop_description = shop_names. shop_description
            data = json.dumps({'shop_name':shop_namez,'shop_phone':shop_phone, 'shop_description':shop_description})
            return HttpResponse(data)
        except:
            return HttpResponse("error") 
    else:
        return HttpResponse("please log in")

    
    return HttpResponse(shop_data)

def product_detail(request, product_id, slug):
    print('product request',request)
    product = get_object_or_404(Product, id=product_id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    return render(request,'shop/product/detail1.html',{'product': product, 'cart_product_form': cart_product_form})







