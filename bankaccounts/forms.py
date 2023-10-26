from django import forms
from bankaccounts.models import KYC
from django.forms import DateInput,FileInput

class DateInput(forms.ModelForm):
    input_type = 'data'

class kyc_form(forms.ModelForm):
    inentify_image = forms.ImageField(widget=FileInput)
    image = forms.ImageField(widget=FileInput)
    signature = forms.ImageField(widget=FileInput)
    class Meta:
        model = KYC
        fields = ['fullname',
                  'image',
                  'marital_status',
                  'gender',
                  'identity_type',
                  'inentify_image',
                  'date_of_birth',
                  'signature',
                  'country',
                  'state',
                  'city',
                  'phone',
                  'email']
        
        widget = {
            'date_of_birth':DateInput
        }