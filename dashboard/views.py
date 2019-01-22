from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from Accounts.models import Account, Shop , Order ,  OrderItem, DeliveryMethod,ShopTransactionActivity , Category , Product
from django.http import HttpResponse
from .forms import WithdrawForm , OrderForm, CreateshopForm ,ProductForm,CategoryForm ,ProductForm2 , CategoryForm2, FrontUIForm
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url= 'login')
def dashboard(request):
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id) 
    except:
        return render (request, 'dashboard.html')

    try:
        
        order = Order.objects.filter(shop_name=shop_name.id)
    except:
        return HttpResponse("you dont have orders yet")

    try:
        transaction = ShopTransactionActivity.objects.filter(shop_name=shop_name.id)
    except:
        return HttpResponse("there are transaction details associated with this order")

    try:
        order_item = OrderItem.objects.filter(order__in=order)
    except:
        return HttpResponse("you dont have order items yet")
    try:
        delivery_method = DeliveryMethod.objects.filter(Order__in=order)
    except:
        return HttpResponse("you dont have a delivery method yet")
    shop_balance = shop_name.shop_balance
    subdomain = shop_name.subdomain

    return render (request, 'dashboard.html',{'order':order,'order_item':order_item ,'delivery_method':delivery_method,'shop_balance':shop_balance,'subdomain':subdomain,'transaction':transaction})

@login_required(login_url= 'login')
def shop_withdraw(request):

    '''
    function to withdraw from shop
    '''
    user = request.user
    user_id = user.id
    try:
        account = Account.objects.get(User=user_id)
    except:
        return HttpResponse('account not found please contact support@oppaly.com')
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
    except:
        return HttpResponse("Shop does not exists")
    shop_balance = shop_name.shop_balance
    shop_phone_number = shop_name.phone_number
    shop_id = shop_name.id
    if request.method == 'POST':
        form_withdraw = WithdrawForm(request.POST)
        if form_withdraw.is_valid():
            clean_form = int(form_withdraw['balance'].value())
            if clean_form > shop_balance:
                return HttpResponse('Enter a balance that is below your shop balance')
            elif clean_form == 0:
                return HttpResponse('you cannot withrdraw  0 balance')
            elif not (clean_form >= 50):
                return HttpResponse('You can only withdraw an amount that is above 50')
            elif shop_balance == 0:
                return HttpResponse('Your balance is low')
            else:
                #shop_balance_form = clean_form
                #mpesa_withdraw_transactions(shop_id, shop_balance_form , shop_phone_number)
                return HttpResponse('This feature is not functional yet')
    else:
        form_withdraw = WithdrawForm()
    return render (request, 'withdraw.html',{'form_withdraw':form_withdraw,'shop_balance':shop_balance})


@login_required(login_url='login')
def refund_order(request):
    '''
    This refund oreders that were already made
    '''
    order_id = request.POST.get('drop')   
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
        shop_id  = shop_name.id
    except:
        return HttpResponse("Shop does not exists")
    try:
        '''
    order = Order.objects.filter(shop_name=shop_name.id, paid = True)
        '''
        order = Order.objects.filter(shop_name=shop_name.id)
    except:
        return HttpResponse("you dont have orders yet")

    try:
        order_item = OrderItem.objects.filter(order__in=order)
    except:
        return HttpResponse("you dont have order items yet")
    if request.method == 'POST':
        try:
            order_itemz = OrderItem.objects.get(pk=order_id, is_refunded = False)
            print(order_itemz)
        except:
            return HttpResponse('could not find the order ')
        try:
            transaction = ShopTransactionActivity.objects.get(order=order_itemz.order.id )
        except:
            return HttpResponse('there are no transactions associated with this shop')
        if transaction.transaction_type == 'Customer_mpesa':

            """
            refund_amount = transaction.transaction_amount
            refund_phone_number = transaction.phone_used
            
            mpesa_refund(shop_id,  refund_amount, refund_phone_number)

            order_itemz.is_refunded = True
            order_itemz.save()
            """
            return HttpResponse('Mpesa refunds are done manually')
        elif transaction.transaction_type == 'Customer_equity':
            print('using equity ')
            refund_amount = transaction.transaction_amount
            refund_phone_number = transaction.phone_used
            payment_transaction_ref = transaction.payment_transaction_ref
            
                #eazzypay_refund(shop_id,  refund_amount, refund_phone_number,payment_transaction_ref, order_itemz.order.id )

                #order_itemz.is_refunded = True
                #order_itemz.save()
            return HttpResponse('Eazzypay refunds are done manually')
        else:
            return HttpResponse('payment method not found')   
        
    return render (request, 'refund.html',{'order':order, 'order_item':order_item})


     




@login_required(login_url= 'login')
def delete_products(request):
    '''
    Delete products 
    '''
    product_id = request.POST.get('drop')   
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
        shop_id  = shop_name.id
    except:
        return HttpResponse("Shop does not exists")
    try:
        categories = Category.objects.filter(shop_name=shop_id)
        print(categories)
    except:
        return HttpResponse('You dont have any categories associated')
    try:
        products = Product.objects.filter(category__in=categories)
    except:
        return HttpResponse('you dont have any products yet')

    if request.method == 'POST':
        print(product_id)
        try:
            delete_product = Product.objects.get(pk=product_id)
            delete_product.delete()
            return HttpResponse(' the product was deleted')
        except:
            return HttpResponse('Product was not found')


    return render (request, 'delete_product.html',{'categories':categories, 'products': products})


"""
@login_required(login_url= 'login')
def product_settings(request):
    # You need to create a model that returns all the products for the shop - with their name,
    #  price, id and other necessary information
    #same applies to the category

    #  

    #more information see product_settings.html
    return render (request, 'product_settings.html')
"""


@login_required(login_url= 'login')
def shop_settings(request):
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
    except:
        return HttpResponse("Shop does not exists")
    subdomain = shop_name.subdomain 
    shopname = shop_name.shop_name
    date_created = shop_name.created
    is_active = shop_name.is_activated
    
    return render (request, 'shop_settings.html', {'subdomain':subdomain, 'shopname':shopname, 'date_created':date_created,'is_active':is_active})


@login_required(login_url= 'login')
def delete_category(request):
    '''
    Delete products 
    '''
    category_id = request.POST.get('drop')   
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
        shop_id  = shop_name.id
    except:
        return HttpResponse("Shop does not exists")
    try:
        categories = Category.objects.filter(shop_name=shop_id)
        print(categories)
    except:
        return HttpResponse('You dont have any categories associated')
    try:
        products = Product.objects.filter(category__in=categories)
    except:
        return HttpResponse('you dont have any products yet')

    if request.method == 'POST':
        print(category_id)
        try:
            delete_product = Category.objects.get(pk=category_id)
            delete_product.delete()
            return HttpResponse(' the category was deleted')
        except:
            return HttpResponse('Category was not found')


    return render (request, 'delete_category.html',{'categories':categories})

@login_required(login_url= 'login')
def delete_shop(request):
     
    return render (request, 'delete_shop.html')

"""
Functions migrated from Accounts app
"""

@login_required(login_url= 'login')
def create_shop(request):
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
        return HttpResponse('you can only create one shop')
    except:
        print('got through this exception')
        if request.method == 'POST':
            formcreateshop = CreateshopForm(request.POST, request.FILES)
            formcreateshopValid = formcreateshop.is_valid()
            if formcreateshopValid:
                createshop = formcreateshop.save(commit=False )
                createshop.Account_id =  account.id
                createshop.save()
            """
            #redirect to dashboard

            """
            return redirect('dashboard:dashboard')
        else:
            formcreateshop = CreateshopForm()
        return render(request, 'shop/createshop.html', {'formcreateshop':formcreateshop})


@login_required(login_url= 'login')
def updateshop(request):
    """
    #Things to do 
    # 1.Give a user choice for the shop the want to update
    # Rename this to add product
    """
    user = request.user
    user_id = user.id
    print(user_id)
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
    except:
        return HttpResponse('you dont have a shop yet, head over to the dashboard and create a shop')
    shop_name_id= shop_name.id
    shopname = shop_name.shop_name
    if request.method == 'POST':
        formproduct = ProductForm(shop_name_id ,request.POST, request.FILES  )
        formproductValid = formproduct.is_valid()
        if formproductValid:
            product = formproduct.save(commit=False)
            clean_form = formproduct['category'].value()
            print('clean form',clean_form)
            category = Category.objects.get(pk=clean_form)
            product.category = category
            product.save()
            """
            #redirect to dashboard
            """
            return redirect('dashboard:dashboard')
    else:
        formproduct = ProductForm(shop_name)
    return render(request, 'shop/updateshop.html', {'formproduct':formproduct})

@login_required(login_url= 'login')
def product_category(request):
    """
    #Things to do 
    # 1.Give a user choice for the shop the want to update
    """
    user = request.user
    user_id = user.id
    print(user_id)
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
    except:
        return HttpResponse('you dont have a shop yet, head over to the dashboard and create a shop')
    if request.method == 'POST':
        formcategory = CategoryForm2(request.POST)
        formproduct = ProductForm2(request.POST,request.FILES)
        if formcategory.is_valid() and formproduct.is_valid():
            category_name = formcategory.cleaned_data['category_name']
            print("category_name", category_name)
            category = Category.objects.create(name = category_name , shop_name = shop_name  )
            product = formproduct.save(commit=False)
            product.category = category
            product.save()
            """
            #redirect to dashboard
            """
            return redirect('dashboard:dashboard')
    else:
        formcategory = CategoryForm2()
        formproduct = ProductForm2()
    return render(request, 'shop/newproduct.html', {'formcategory':formcategory,'formproduct':formproduct})

@login_required(login_url= 'login')
def front_ui(request):
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    shop_name = Shop.objects.get(Account_id=account.id)
    print(shop_name)
    if request.method == 'POST':
        formcreateshop = FrontUIForm(request.POST,request.FILES)    
        if formcreateshop.is_valid():
            shop_ui = formcreateshop.cleaned_data['shop_banner']
            shop_name.shop_banner = shop_ui
            shop_name.save()
            """
            parse out the form and update 
            the shop with banner and logo on its shop_name instance
            #redirect to dashboard
            """
            return redirect('dashboard:dashboard')
    else:
        formcreateshop = FrontUIForm()
    return render(request, 'shop/frontUI.html', {'formcreateshop':formcreateshop})

@login_required(login_url= 'login')
def profile(request):
    user = request.user
    user_id = user.id
    account = Account.objects.get(User=user_id)
    try:
        shop_name = Shop.objects.get(Account_id=account.id)
        paid = shop_name.paid
        activated = shop_name.is_activated
        shop_names = shop_name.shop_name
    except:
        first_name = account.first_name
        last_name = account.last_name
        email = account.email
        company_name = account.company_name
        phone_number = account.phone_number
        created = account.created
        return render (request, 'profile.html',{'first_name':first_name,'last_name':last_name,
         'company_name':company_name, 'phone_number':phone_number, 'created':created, 'email':email })
    first_name = account.first_name
    last_name = account.last_name
    email = account.email
    company_name = account.company_name
    phone_number = account.phone_number
    created = account.created
    return render (request, 'profile.html',{'first_name':first_name,'last_name':last_name,
         'company_name':company_name, 'phone_number':phone_number, 'created':created,
         'shop_name':shop_names, 'paid':paid , 'activated':activated,'email':email })







