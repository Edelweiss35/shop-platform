from django import forms

from Accounts.models import Order , DeliveryMethod


class OrderCreateForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }
    ))
    

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email'
        }
    ))


    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Address'
        }
    ))

    postal_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Postal Code'
        }
    ))

    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }
    ))


    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']



  
class DeliveryMethodForm(forms.ModelForm):
    '''

   deliver_method = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
            
        }
    ))
    '''





    class Meta:
        
        model = DeliveryMethod

        fields = ['delivery_method']
   
