from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import  authenticate, login
from .forms import SignUpForm, CreateshopForm , CampaignForm
from Accounts.models import Account, Shop , Product ,Category , Campaign
from django.template import RequestContext
from cart.forms import CartAddProductForm
from storefront import views 
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.conf import settings 
import json
from django.contrib.auth import get_user_model

def home(request):
    campaign_form = CampaignForm()
    try:
        print('homepage',request.shop_details)
    except:
        return render (request, 'home.html', {'home':'home','campaign_form':campaign_form })
    if request.active == False:
        try:
            shop_name = Shop.objects.get(pk=request.shop_details)
        except:
            return HttpResponse(" We can not find your shop details")

        shop_namez = shop_name.shop_name
        shop_logo = shop_name.shop_logo
        shop_phone = shop_name.phone_number
        shop_banner = shop_name.shop_banner
        try:
            categories = Category.objects.filter(shop_name=request.shop_details)
        except:
            return HttpResponse("there are no product categories associated with your shop")
        try:
            products = Product.objects.filter(category__in=categories).all()
        except:
            return HttpResponse("there are no product categories associated with your shop")


        return render (request, 'shop/list1-test.html', {'categories':  categories,'products':products,'shop_banner':shop_banner,
            'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone})
    else:
        try:
            shop_name = Shop.objects.get(pk=request.shop_details)
        except:
            return HttpResponse(" We can not find your shop details")
        shop_namez = shop_name.shop_name
        shop_logo = shop_name.shop_logo
        shop_phone = shop_name.phone_number
        shop_banner = shop_name.shop_banner
        try:
            categories = Category.objects.filter(shop_name=request.shop_details)
        except:
            return HttpResponse("there are no product categories associated with your shop")
        try:
            products = Product.objects.filter(category__in=categories).all()
        except:
            return HttpResponse("there are no product categories associated with your shop")
        
        return render(request, 'shop/list1.html', {'categories':  categories,'products':products,'shop_banner':shop_banner,
            'shop_namez':shop_namez,'shop_logo':shop_logo,'shop_phone':shop_phone})

def home_api(request):
    try:
        print('homepage',request.shop_details)
    except:
        shop_data = {'error':'shop not found'}
        return JsonResponse(shop_data)
    shop_name = Shop.objects.get(pk=request.shop_details)
    shop_namez = shop_name.shop_name
    shop_phone = shop_name.phone_number
    shop_description = shop_name.shop_description
    shop_data = json.dumps({'shop_name':shop_namez,'shop_phone':shop_phone, 'shop_description':shop_description})
    return HttpResponse(shop_data)
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        User = get_user_model()
        if form.is_valid():
            User = get_user_model()
            User = form.save()
            login(request, User)
            

            return redirect('dashboard:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def campaign(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
            
        except:
            return JsonResponse({
            'status': 1,
            'error': 'No JSON object could be decoded'
            })

        try:
            phone_number = req_data['phone_number']
            fullname = req_data['fullname']
            message = req_data['message']
            email = req_data['email']
        except:
            print ('not going through')
            return JsonResponse({'status': 300, 'error': 'Invalid request.'})

        Campaign.objects.create(fullname = fullname,
                                email_address = email,
                                phone_number = phone_number,
                                message = message
                                )
        subject = 'Welcome to the Oppaly platform'
        message = 'Dear {},\n\n Thank you for your interest in Oppaly, we will contact you shortly. In the meantime here is a link https://oppaly.com/Account/how-to guide on how to create your shop .'.format(fullname )

        try:
            send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email])
        except:
            print('email does not work')
        return JsonResponse({'status': 200, 'response': 'Thank you'})
    else:
        return redirect('home')

def how_to(request):
    print(settings.DEFAULT_FROM_EMAIL)
    return render (request, 'how-to.html')
