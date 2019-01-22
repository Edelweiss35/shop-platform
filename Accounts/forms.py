from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from Accounts.models import Shop, Category, Product
from django import forms
from django.core.exceptions import ValidationError
from Accounts.models import Account
from django.contrib.auth import get_user_model

class SignUpForm(forms.Form):


    

    first_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
            }))

    last_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
            }))

    email = forms.CharField(label='', max_length=254, required=True, widget=forms.EmailInput( 
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
            }))

    phone_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '+254'
            }))

    company_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'company name or business name'
            }))

    

    password1 = forms.CharField(label='',max_length=32, widget=forms.PasswordInput( 
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
            }))

    password2 = forms.CharField(label='', max_length=32,widget=forms.PasswordInput( 
        attrs={
            'class': 'form-control',
            'placeholder': ' Confirm Password'
            }))

   

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        User = get_user_model()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_company(self):
        company_name = self.cleaned_data['company_name'].lower()
        return company_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].lower()
        return last_name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        User = get_user_model()
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )

         
        Account.objects.create(User=user,
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            company_name = self.cleaned_data['company_name'],
            phone_number = self.cleaned_data['phone_number'],
            email= self.cleaned_data['email']
        )
        
       
        return user


class CreateshopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name','subdomain','shop_description','shop_banner', 'phone_number']

class CampaignForm(forms.Form):
    fullname = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
            }))
    
    email=forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
            }))

    phone_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
            }))
            
    message = forms.CharField(label='', max_length=100,widget=forms.Textarea (
        attrs={
            'class': "form-control",
            'placeholder': 'Message'
            }))