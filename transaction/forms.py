from django import forms
from transaction.models import CreditCard

class CredictCardForms(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name','number','month','year','CVV','card_type',]