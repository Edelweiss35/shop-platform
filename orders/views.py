from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from cart.cart import Cart
from orders.forms import OrderCreateForm , DeliveryMethodForm
from Accounts.models import OrderItem ,Shop ,Order
from orders.task import order_created
from django.http import HttpResponse , JsonResponse
from cart.cart import Cart
from cart.forms import CartAddProductForm
from json import dumps, loads, JSONEncoder, JSONDecoder
from django.core import serializers
import pickle
import json
from django.http import HttpResponse

from base64 import b64encode, b64decode





def order_create(request):
    """
    #link this order to the shop

    """
    value = getattr(request,'shop_details', None)

    active = getattr(request,'active', None)

    if active == False:
        return HttpResponse('The shop is not activate contact support@oppaly.com')

 
    
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if value is not None:
                order = form.save(commit= False)
                shop  = Shop.objects.get(pk=value)
                order.shop_name = shop
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
                cart.clear()
                print('create order ', order.id)
                request.session['order_id'] = order.id
                order_id = order.id
                
                return redirect('orders:delivery_method')
            else:
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
                cart.clear()
                print('create order ', order.id)
                request.session['order_id'] = order.id
                order_id = order.id
                print('went through')
                return redirect('orders:delivery_method')
    else:
        form = OrderCreateForm()
    return render(request,'checkout1.html',{'cart': cart, 'form': form})


def delivery_method(request):
    order_id = request.session.get('order_id')
    print(order_id)
    if request.method == 'POST':
        form = DeliveryMethodForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            order = Order.objects.get(pk=order_id)
            delivery.Order = order
            delivery= form.save()
     
            return redirect('orders:order_review')
    else:
        form = DeliveryMethodForm()
    return render(request , 'delivery.html', {'form':form } )

def order_review(request):
    order_id = request.session.get('order_id')
    order_ = Order.objects.get(pk=order_id)
    order_item = OrderItem.objects.filter(order=order_)
    print(order_item)

   
    return render(request,'checkout4.html', {'order_item':order_item})

def order_review_api(request):
    try:
        order_id = request.session.get('order_id')
    except:
        return JsonResponse({'response': " there is no order made 1"})
    try:
        order_ = Order.objects.get(pk=order_id)
    except:
        return JsonResponse({'response': " there is no order made 2"})


    try: 
        order_item = OrderItem.objects.filter(order=order_)
        data = serializers.serialize("json", order_item)
    except:
        return JsonResponse({'response': " there is no order made 3"})
    
    return HttpResponse({data})
