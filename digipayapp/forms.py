from django import forms
from digipayapp.models import user_profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField

class pay_form(forms.ModelForm):
    password = forms.CharField(max_length=200,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class user_profile_form(forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ['user_img']


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    captcha = ReCaptchaField()
    