from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from digipayapp.forms import user_profile_form,user_profile,pay_form,UserRegisterForm,pay_form
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bankaccounts.models import KYC,Account
 


# Create your views here.

@login_required(login_url='digipayapp:signin')
def user_logout(request):
    logout(request)
    return redirect("digipayapp:user_login")


def reg(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"hey {username} your account was created successfully.")
    else:
        form = UserRegisterForm()
    return render(request,"account/reg.html",{'form':form})




def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        print(username,password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('bankaccounts:account')
        else:
            return HttpResponse("check your credentials...!")
    return render(request,"account/signin.html")



