from django.shortcuts import render,redirect
from bankaccounts.forms import kyc_form
from bankaccounts.models import User,Account,KYC
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from transaction.forms import CredictCardForms
from transaction.models import Transaction,CreditCard

# Create your views here.
@login_required(login_url='digipayapp:signin')
def account(request):
    kyc = KYC.objects.get(user = request.user)
    account = KYC.objects.get(user = request.user)
    context = {
        'kyc' : kyc,
        'account':account

    }

    
    return render(request,'account/account.html',context)



def kyc_reg(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == 'POST':
        form = kyc_form(request.POST,request.FILES,instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request,'KYC form submitted successfully , In review now')
            return redirect('kyc')
    else:
        form = kyc_form(instance=kyc)
    context = {
            'account' : account,
            'form':form,
            'kyc':kyc,
        }
    
    return render(request,'account/kyc_form.html',context)


def user_logout(request):
    logout(request)
    return redirect('bankaccounts:signin')

def dashboard(request):
    user=request.user
    account=Account.objects.get(user=user)
    transaction=Transaction.objects.all()
    Credict_card = CreditCard.objects.all()
    form = CredictCardForms()
    if request.method == 'POST':
        form = CredictCardForms(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'account':account,
        'transaction':transaction,
        'form':form,
        'Credict_card':Credict_card
    }
    return render(request,'account/dashboard.html',context)
