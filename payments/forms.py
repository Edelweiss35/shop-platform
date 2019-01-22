from django import forms

class MpesaForm(forms.Form):
    fullname = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }))
    phone_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '0782456789'
        }))

class EquityForm(forms.Form):
    eazzy_fullname = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }))
    eazzy_phone_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '0782456789'
        }))

class Visa_Mc_Form(forms.Form):

    visa_mc_fullname = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }))
    visa_mc_card_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'card number'
        }))

    visa_mc_expiry = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': ' exipry date ex 2490'
        }))
    
    visa_mc_cvv = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'cvv ex. 234'
        }))

    visa_mc_phone_number = forms.CharField(label='', max_length=100,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '0782456789'
        }))