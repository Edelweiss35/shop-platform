from django import forms
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import json
from cart.forms import CartAddProductForm
from Accounts.models import Category, Product
from django.http import JsonResponse
from Accounts.models import Account, Shop , Product ,Category
from django.http import HttpResponse

class ChoiceForm(forms.Form):
    shop = forms.ModelChoiceField(queryset=None,empty_label=None, widget=forms.RadioSelect)

    
    def __init__(self, account_id, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(Account_id=account_id) 

   
