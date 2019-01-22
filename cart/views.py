from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Accounts.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.core import serializers




@require_POST
def cart_add(request, product_id):
    print('product',product_id)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'detail1.html', {'cart': cart})


def order_cart_detail(request):
    cart = Cart(request)
   
    data = []
    for item in cart:
        data.append(item['quantity'])
        data.append(item['price'])
        data.append(str(item['product']))
        data.append(item['total_price'])

       
    dataz = json.dumps(data)
    return JsonResponse(dataz , safe=False)




        


    

