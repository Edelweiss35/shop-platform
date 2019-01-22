from django.shortcuts import render
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render, get_object_or_404 , redirect
from Accounts.models import Order,ShopTransactionActivity , Shop
import threading
import requests
from requests.auth import HTTPBasicAuth
from .forms import MpesaForm , EquityForm , Visa_Mc_Form
from django.http import HttpResponse , JsonResponse
import json
from django.conf import settings 
import uuid
import logging
from orders.task import order_created
from sentry_sdk.integrations.logging import LoggingIntegration


"""
def gateway_keys():
    data = { "username":settings.USERNAME,"password":settings.PASSWORD }
    headers={'Content-Type':'application/x-www-form-urlencoded',
         'authorization': settings.AUTHORIZATION
        }
    api="https://uat.jengahq.io/identity/v2/token"
    r = requests.post(api, headers=headers, data = data)
    res = r.json()
    global access_token
    try:
        access_token = res['access_token']
    except:
        access_token = '00000000000000000'
        logging.error("An exception happened , jenga api not working", exc_info=True)
        return access_token
    return access_token
def update_key():
    gateway_keys()
    update = threading.Timer(2500, update_key).start()
    return update

update_key()
"""







def request_signing(arg1):
    message = arg1
    encoded  = message.encode('ascii')
    encoded_message  = base64.b64encode(encoded) 
    key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, settings.PEM)
    sign1=OpenSSL.crypto.sign(key, encoded_message, "sha256")
    signature = base64.b64encode(sign1).decode()
    return signature
 
def mobile_wallet_commision(arg1):
    percent = arg1 * 0.02
    total_commision = percent
    result = arg1 - total_commision
    print(result)
    return result
   
def visa_mc_commision(arg1):
    percent = arg1 * 0.04
    total_commision = percent + 4
    result = arg1 - total_commision
    print(result)
    return result
    
"""
def mpesa_withdraw_transactions(arg1, arg2, arg3):
    '''
    mpesa withdraw
    '''
    shop_id = arg1
    value = arg1
    print(shop_id)
    shop_phone_number = str(arg3)
    phone_used = shop_phone_number 
    shop_balance = int(arg2)
    withdraw_amount = shop_balance 
    print(shop_balance)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = { "Authorization": "Bearer %s" % mpesa_access_token }
    request_to_be_sent =  {
        "ShortCode": "600737",
        "CommandID": "CustomerPayBillOnline",
        "Amount": withdraw_amount,
        "Msisdn": phone_used,
        "BillRefNumber": "35346"
    }
    ri = json.dumps(request_to_be_sent)
    payload = json.loads(ri)
    response = requests.post(api_url, json = payload, headers=headers)
    Mpesa_response = str(response.json())
    global mpesa_paid_withdraw 
    if response.status_code == 200:
        print('went through')
        if value is not None:
            mpesa_paid_withdraw = True
            Shopx = Shop.objects.get(pk=value)
            shop_name = Shopx.shop_name
            shop_balance = Shopx.shop_balance
            update_shop_balance = shop_balance - withdraw_amount
            Shopx.shop_balance = update_shop_balance
            Shopx.payment_response =  Mpesa_response
            Shopx.save()

            

            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = withdraw_amount,
            payment_response =  Mpesa_response,
            transaction_type = 'withdraw_from_shop',
            phone_used = phone_used,
            order = None,
            is_rejected = False)
            return mpesa_paid_withdraw
        else:
            mpesa_paid_withdraw = True
    else:
        mpesa_paid_withdraw = False
        print('passsed herree')
        Shopx = Shop.objects.get(pk=value)
        ShopTransactionActivity.objects.create(shop_name = Shopx,
        transaction_amount = withdraw_amount,
        payment_response =  Mpesa_response,
        transaction_type = 'withdraw_from_shop',
        phone_used = phone_used,
        order = None,
        is_rejected = True)
        return mpesa_paid_withdraw
    return mpesa_paid_withdraw
    

"""
"""
def mpesa_refund(arg1, arg2, arg3):
    shop_id = arg1
    value = arg1
    print(shop_id)
    refund_phone_number = str(arg3)
    refund_amount = int(arg2)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = { "Authorization": "Bearer %s" % mpesa_access_token }
    request_to_be_sent =  {
        "ShortCode": "600737",
        "CommandID": "CustomerPayBillOnline",
        "Amount": refund_amount,
        "Msisdn":  refund_phone_number,
        "BillRefNumber": "35346"
    }
    ri = json.dumps(request_to_be_sent)
    payload = json.loads(ri)
    response = requests.post(api_url, json = payload, headers=headers)
    Mpesa_response = str(response.json())
    global mpesa_refund_paid 
    if response.status_code == 200:
        if value is not None:
            mpesa_refund_paid = True
            Shopx = Shop.objects.get(pk=value)
            shop_name = Shopx.shop_name
            shop_balance = Shopx.shop_balance
            update_shop_balance = shop_balance - refund_amount
            Shopx.shop_balance = update_shop_balance
            Shopx.payment_response =  Mpesa_response
            Shopx.save()

            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = refund_amount,
            payment_response =  Mpesa_response,
            transaction_type = 'refund_order',
            phone_used = refund_phone_number,
            order = None,
            is_rejected = False)
            return mpesa_refund_paid
        else:
            mpesa_refund_paid = True
    else:
        mpesa_refund_paid = False
        Shopx = Shop.objects.get(pk=value)
        ShopTransactionActivity.objects.create(shop_name = Shopx,
        transaction_amount = refund_amount,
        payment_response =  Mpesa_response,
        transaction_type = 'refund_order',
        phone_used = refund_phone_number,
        order = None,
        is_rejected = True)
        return mpesa_refund_paid
    return mpesa_refund_paid


def eazzypay_refund(arg1, arg2, arg3, arg4, arg5):
    shop_id = arg1
    value = arg1
    payment_ref_number = arg4
    order_id = arg5
    refund_phone_number = str(arg3)
    refund_amount = int(arg2)
    print(refund_phone_number)
    print(refund_amount)
    internal_reference_number = str(uuid.uuid4())
    description = str({'shop name ':shop_id, 'refund_order_id':order_id, 'refund_for':refund_phone_number, 'reference_number':internal_reference_number})
    refund_description = json.dumps(description)
    payload  = {"transaction":{"reference":payment_ref_number,"amount":refund_amount,"service":"EazzyPayOnline","channel":"EAZ","description":refund_description,"type":"refund"},"customer":{"mobileNumber": refund_phone_number,"countryCode":"KE"}}
    headers = {
    "Authorization": "Bearer %s" % access_token,
    'content-type': "application/json",
    'signature': signature_sandbox
    }
    api = "https://sandbox.jengahq.io/transaction-test/v2/payments/refund"
    data = json.dumps(payload)
    try:
        response = requests.post(api, headers=headers, data=data)
    except:
        return JsonResponse({'error':'check your internet conectivity','status':'300'})
    response_json = response.json()
    try:
        status = response_json['SUCCESS']
        reference_number = response_json['reference']
    except:
        return JsonResponse({'error':'payment did not go through','status':'300'})
    if status == 'SUCCESS':
        equity_refund_paid = True
        Shopx = Shop.objects.get(pk=value)
        shop_name = Shopx.shop_name
        shop_balance = Shopx.shop_balance
        update_shop_balance = shop_balance - refund_amount
        Shopx.shop_balance = update_shop_balance
        Shopx.payment_response = response_json
        Shopx.save()
        ShopTransactionActivity.objects.create(shop_name = Shopx,
        transaction_amount = refund_amount,
        payment_response =  response_json,
        transaction_type = 'refund_order',
        phone_used = refund_phone_number,
        payment_transaction_ref = reference_number,
        order_transaction_ref = internal_reference_number,
        order = None,
        is_rejected = False)
        return JsonResponse({'status':'200', 'response':"trasaction was succesfull"})  
"""
   
    
def mpesa_ecom_transaction(request):
    value = getattr(request,'shop_details', None)

    active = getattr(request,'active', None)

    if active == None:
        return HttpResponse('The shop is not activate contact support@oppaly.com')

    '''
    mpesa ecomerce transaction
    '''
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({
            'status': 1,
            'error': 'No JSON object could be decoded'
            })

        try:
            phone_used  = req_data['phone_number']
            fullname = req_data['fullname']
        except Exception as e:
            return JsonResponse({'status': '300', 'error': 'Invalid request.'})
        try:
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            shop_id = order.shop_name
            sale_amount =  order.get_total_cost()
        except:
            return JsonResponse({'status': '300', 'error': 'Invalid order.'})
        description = str({'shop name ':shop_id, 'order_id':order_id, 'order_placed_by':fullname})
        order_description = json.dumps(description)
        phone_used = str(phone_used)
        sale_amount = int(sale_amount)
        internal_reference_number = str(uuid.uuid4())
        payload = {"customer":{"mobileNumber":phone_used,"countryCode":"KE"},
        "transaction":{"amount":sale_amount,"description":order_description,"reference":internal_reference_number,"businessNumber":"55"}}
        headers = {
            "Authorization": "Bearer %s" % access_token,
            'content-type': "application/json"
            }
        api="https://uat.jengahq.io/transaction/v2/payment/mpesastkpush"
        data = json.dumps(payload)
        try:
            response = requests.post(api, headers=headers, data=data)
        except:
            return JsonResponse({'error':'check your internet conectivity','status':'300'})
        response_json = response.json()
        try:
            status = response_json['SUCCESS']
            reference_number = response_json['referenceNumber']
        except:
            return JsonResponse({'error':'payment did not go through','status':'300'})
        if status == 'SUCCESS':
            order.paid = True
            order.save()
            Shopx = Shop.objects.get(pk=value)
            shop_name = Shopx.shop_name
            shop_balance = Shopx.shop_balance
            mpesa_commision = mobile_wallet_commision(sale_amount)
            update_shop_balance = shop_balance + mpesa_commision
            Shopx.shop_balance = update_shop_balance
            Shopx.save()
            
            order_created(order_id)
            

            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            transaction_type = 'MPESA',
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            phone_used = phone_used,
            order = order,
            is_rejected = False)
            return JsonResponse({'status':'200', 'response':"trasaction was succesfull"})  
        else:
            order.paid = False
            order.save()
            Shopx = Shop.objects.get(pk=value)
            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            transaction_type = 'MPESA',
            phone_used = phone_used,
            order = order,
            is_rejected = True)
            return JsonResponse({'error':response_json ,'status':'300'})
    return JsonResponse({'status': -1, 'error': 'Invalid request.'})
        


def eazzypay_ecom(request):
    value = getattr(request,'shop_details', None)
    active = getattr(request,'active', None)

    if active == None:
        return HttpResponse('The shop is not activate contact support@oppaly.com')

    '''
    equity/eazzy ecomerce transaction
    '''
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
            print(req_data)
        except:
            return JsonResponse({
            'status': 1,
            'error': 'No JSON object could be decoded'
            })

        try:
            phone_used  = req_data['phone_number']
            fullname = req_data['fullname']
        except Exception as e:
            return JsonResponse({'status': 300, 'error': 'Invalid request.'})
        try:
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            shop_id = order.shop_name
            sale_amount =  order.get_total_cost()
        except:
            return JsonResponse({'status': -1, 'error': 'Invalid order.'})
        description = str({'shop_id':shop_id, 'order_id':order_id,'order_placed_by':fullname})
        order_description = json.dumps(description)
        phone_used = str(phone_used)
        sale_amount = int(sale_amount)
        internal_reference_number = str(uuid.uuid4())
        countryCode = 'KE'

        message = internal_reference_number + sale_amount + settings.USERNAME+countryCode
        eazzy_signature=request_signing(message)
 
        payload = {"customer":{"mobileNumber":phone_used,"countryCode":"KE"},
        "transaction":{"amount":sale_amount,"description":order_description,"type":"EazzyPayOnline","reference":internal_reference_number}}
        headers = {
            "Authorization": "Bearer %s" % access_token,
            'content-type': "application/json",
            'signature': eazzy_signature
            }
        api="https://uat.jengahq.io/transaction/v2/payments"
        data = json.dumps(payload)
        try:
            response = requests.post(api, headers=headers, data=data)
        except:
            return JsonResponse({'error':'check your internet conectivity','status':'300'})
        response_json = response.json()
        print(response.json())
        print(phone_used)
        try:
            status = response_json['status']
            reference_number = response_json['referenceNumber']
        except:
            return JsonResponse({'error':'payment did not go through','status':'300'})
        if status == 'SUCCESS':
            order.paid = True
            order.save()
            Shopx = Shop.objects.get(pk=value)
            shop_balance = Shopx.shop_balance
            eazzy_commision = mobile_wallet_commision(sale_amount)
            update_shop_balance = shop_balance + eazzy_commision
            Shopx.shop_balance = update_shop_balance
            Shopx.save()

            order_created(order_id)

            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            transaction_type = 'Eazzypay',
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            phone_used = phone_used,
            order = order,
            is_rejected = False)
            return JsonResponse({'status':'200', 'response':"trasaction was succesfull"})  
        else:
            order.paid = False
            order.save()
            Shopx = Shop.objects.get(pk=value)
            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            transaction_type = 'Eazzypay',
            phone_used = phone_used,
            order = order,
            is_rejected = True)
            return JsonResponse({'error':'payment did not go through','status':'300'})
    return JsonResponse({'status': -1, 'error': 'Invalid request.'})
        

def visa_mc(request):
    value = getattr(request,'shop_details', None)

    active = getattr(request,'active', None)

    if active == None:
        return HttpResponse('The shop is not activate contact support@oppaly.com')
    '''
    visa and master ecomerce transaction
    '''
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({
            'status': 1,
            'error': 'No JSON object could be decoded'
            })
        try:
            phone_used  = req_data['phone_number']
            fullname = req_data['fullname']
            expiry = req_data['expiry']
            card_number = req_data['card_number']
            cvv = req_data['cvv']
            order_expiry_date = req_data['order_expiry_date']
            transaction_valueDate = req_data['transaction_valueDate']
            transaction_date = req_data['transaction_date']
            transaction_postedDate = req_data['transaction_postedDate']
        except Exception as e:
            return JsonResponse({'status': '300', 'error': 'Invalid request.'})
        try:
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            shop_id = order.shop_name
            sale_amount =  order.get_total_cost()
        except:
            return JsonResponse({'status': '300', 'error': 'Invalid order.'})
        description = str({'shop_id':shop_id, 'order_id':order_id,'order_placed_by':fullname})
        order_description = json.dumps(description)
        phone_used = str(phone_used)
        sale_amount = int(sale_amount)
        internal_reference_number = str(uuid.uuid4())

        """
        message = ""
        visa_signature = request_signing(message)
        
        """

        payload = {"transaction":{"amount":sale_amount,"currency":"kes","orderRef":order_id,"orderExpiry":order_expiry_date,
        "reference":internal_reference_number,"description":order_description,"billerCode":"900900","valueDate":transaction_valueDate,"date":transaction_date,
        "postedDate":transaction_postedDate},"card":{"number":card_number,"expiry":expiry,"securityCode":cvv},
        "customer":{"name":fullname,"customerid":fullname,"mobileNumber":phone_used}}
        headers = {
            "Authorization": "Bearer %s" % access_token,
            'content-type': "application/json",
            
            }
        api="https://uat.jengahq.io/transaction/v2/migs/payment"
        data = json.dumps(payload)
        try:
            response = requests.post(api, headers=headers, data=data)
        except:
            return JsonResponse({'error':'check your internet conectivity','status':'300'})
        response_json = response.json()
        print(response.json())
        try:
            status = response_json['status']
            reference_number = response_json['transactionId']
        except:
            return JsonResponse({'error':'payment did not go through','status':'300'})
        if status == 'SUCCESS':
            order.paid = True
            order.save()
            Shopx = Shop.objects.get(pk=value)
            shop_balance = Shopx.shop_balance
            commision_visa = visa_mc_commision(sale_amount)
            update_shop_balance = shop_balance +  commision_visa
            Shopx.shop_balance = update_shop_balance
            Shopx.save()

            order_created(order_id)

            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            transaction_type = 'Eazzypay',
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            phone_used = phone_used,
            order = order,
            is_rejected = False)
            return JsonResponse({'status':'200', 'response':"trasaction was succesfull"})  
        else:
            order.paid = False
            order.save()
            Shopx = Shop.objects.get(pk=value)
            ShopTransactionActivity.objects.create(shop_name = Shopx,
            transaction_amount = sale_amount,
            payment_response =  response_json,
            payment_transaction_ref = reference_number,
            order_transaction_ref = internal_reference_number,
            transaction_type = 'Eazzypay',
            phone_used = phone_used,
            order = order,
            is_rejected = True)
            return JsonResponse({'error':'payment did not go through','status':'300'})
    return JsonResponse({'status': -1, 'error': 'Invalid request.'})
        

def pay_on_delivery(request):
    value = getattr(request,'shop_details', None)
    active = getattr(request,'active', None)

    if active == None:
        return HttpResponse('The shop is not activate contact support@oppaly.com')

    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({
            'status': 1,
            'error': 'No JSON object could be decoded'
            })
        try:
            message = req_data['POD']
            print(message)
        except:
            return JsonResponse({'error':'payment did not go through','status':'300'})
        try:
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            sale_amount =  order.get_total_cost()
        except:
            return JsonResponse({'status': '300', 'error': 'Invalid order.'})
        internal_reference_number = str(uuid.uuid4())
        order.paid = False
        order.save()
        Shopx = Shop.objects.get(pk=value)
        shop_balance = Shopx.shop_balance
        Shopx.shop_balance =  shop_balance
        Shopx.save()

        order_created(order_id)
        
        ShopTransactionActivity.objects.create(shop_name = Shopx,
        transaction_amount = sale_amount,
        payment_response =  None,
        transaction_type = 'POD',
        payment_transaction_ref = None,
        order_transaction_ref = internal_reference_number,
        phone_used = None,
        order = order,
        is_rejected = False)
        return JsonResponse({'status':'200', 'response':"trasaction was succesfull"})  

        

'''
This is for merchant to withdraw to equity bank

def equity_withdraw_transaction(request):
    user = request.user
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({'status': -1,
            'error': 'No JSON object could be decoded'
            })
    try:
        shop_name =  data['shop_name']
    except Exception as e:
        return JsonResponse({'status': -1, 'error': 'Invalid request.'})
    shop = Shop.objects.filter(shop_name=shop_name).first()
    if not shop:
        return JsonResponse(
            {'status': -1, 'error': 'Shop not found.'})
    if shop.shop_balance == 0:
        return JsonResponse(
            {'status': -1, 'error': 'You dont have enough funds to withdraw.'})
    withdraw_amount = int(shop.shop_balance)
    merchant_phone = str(user.phone)
    api_url = "https://api.equitybankgroup.com/transaction-sandbox/v1-sandbox/remittance"
    headers = { "Authorization": "Bearer %s" % access_token,
             'Content-Type':'application/json'}
    request_to_be_sent = {
    "source": {
        "countryCode": "KEN",
        "name": "JOSHUA DOE",
        "accountNumber": "12365489"
    },
    "destination": {
        "type": "Swift remit",
        "countryCode": "524",
        "name": "WILLIAM DOE",
        "cardNumber": "245",
        "bankCode": "123",
        "bankBic": "123",
        "accountNumber": "24524565",
        "mobileNumber": merchant_phone,
        "walletName": "My Wallet"
    },
    "transfer": {
        "type": "withdraw from shop",
        "amount": withdraw_amount,
        "currencyCode": "KES",
        "reference": "3241235236",
        "date": "04052018",
        "description": "wert"
    }
    }
    r = json.dumps(request_to_be_sent)
    payload = json.loads(r)
    response = requests.post(api_url, json = payload, headers=headers)
    equity_response = str(response.json())
    if response.status_code == 200:
        Shop_Transactions.objects.create(shop_name = shop,
        transaction_amount = withdraw_amount,
        customer_phone_used = merchant_phone,
        transaction_type = 'withdraw_from_shop',
        payment_response =  equity_response,
        is_rejected = False)
        return JsonResponse({'status': 1, 'amount withdrawn':withdraw_amount, 'withdrawn_to': merchant_phone})
    else:
        Shop_Transactions.objects.create(shop_name = shop,
        transaction_amount = withdraw_amount,
        customer_phone_used = merchant_phone,
        transaction_type = 'withdraw_from_shop',
        payment_response =  equity_response,
        is_rejected = True)
    return JsonResponse({'status': -1, 'could not withdraw to this phone': merchant_phone , "amount to be withdrawn": withdraw_amount})
'''

def payment_process(request):
    equity_form = EquityForm()
    visa_mc_form = Visa_Mc_Form()
    mpesa_form = MpesaForm()
    return render(request, 'payment_process.html',{'mpesa_form':mpesa_form, 'equity_form':equity_form ,'visa_mc_form':visa_mc_form })




@csrf_exempt
def payment_done(request):
    return render(request, 'checkout5.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

