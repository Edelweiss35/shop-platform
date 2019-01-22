from Accounts.models import Order, OrderItem , ShopTransactionActivity
from django.forms import ModelForm
from django import forms
from Accounts.models import Shop, Category, Product
from django.utils.text import slugify
import itertools 






class OrderForm(ModelForm):
    
    class Meta:
        model =  OrderItem
        fields = ['order']
       
   
    def __init__(self, order_id, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].queryset  = Order.objects.filter(order__in=order_id)
    



class WithdrawForm(forms.Form):
    balance = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        
        }))

class CreateshopForm(ModelForm):

    shop_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'shop name'
        
        }))

    

    class Meta:
        model = Shop
        fields = ['shop_name','shop_description','shop_banner', 'phone_number']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        

class ProductForm(ModelForm):
        class Meta:
            model = Product
            fields = ['name','image','description','price','stock','category']

        def __init__(self, shop_name_id, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['category'].queryset = Category.objects.filter(shop_name=shop_name_id)
        
        

class CategoryForm2(forms.Form):
    category_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        
        }))

    

class ProductForm2(ModelForm):
    name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        
        }))


    class Meta:
        model = Product
        fields = ['name','image','description','price','stock']
    


    

    


class FrontUIForm(forms.Form):
    shop_banner  = forms.ImageField()
   
   
