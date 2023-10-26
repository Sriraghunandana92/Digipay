from django.shortcuts import render
from transaction.models import Transaction,CreditCard
from bankaccounts.models import Account,KYC
from django.contrib import messages
from django.shortcuts import redirect

def credit_card(request,number):
    account = Account.objects.get(user=request.user)
    kyc = KYC.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(number=number)
    context = {
        'credict_card':credit_card,
        'account':account,
        'kyc':kyc
    }
    return render(request,'account/credit_card_detail.html',context)

def credit_card_bill(request,card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id)
    context = {
        'account':account,
        'credit_card':credit_card
    }
    if request.method == "POST":
        if account.account_balance > credit_card.amount:
            credit_card.amount +=account.account_balance
            credit_card.save()
            account.account_balance -= credit_card.amount
            account.save()
            return redirect("transactions:send_card_bill",credit_card.number)
        else:
            messages.warning(request,"Insufficient Funds, Fund your account and try again")
    return render(request,"account/credit_card_bill.html",context)

def withdraw_amount(request,card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id)
    amount = request.POST.get("amount")
    context = {
        'account':account,
        'credit_card':credit_card,
        'amount':amount
    }
    if request.method == 'POST':
        if credit_card.amount > 0 and amount:
            credit_card.amount -= int(amount)
            credit_card.save()
            account.balance += int(amount)
            account.save()
            return redirect("transactions:credit_card",credit_card.number)
        else:
            messages.warning(request,"Insufficient Funds, fund your account and try again")
    return render(request, "account/withdraw_amount.html",context)

def credit_card_delete(request,card_id):
    account = Account.objects.get(user = request.user)
    credit_card = CreditCard.objects.get(card_id=card_id)

    context = {
        'account':account,
        'credit_card':credit_card
    }
    if credit_card.amount > 0:
        account.account_balance +=credit_card.amount
        account.save()
        credit_card.delete()
        messages.warning(request,"Credit card Delete Successfully")
        return redirect("bankaccounts:dashboard")
    elif credit_card.amount == 0 :
        credit_card.delete()
        messages.warning(request,"Credit card Deleted Successfully")
        return redirect("account:dashboard")
    return render(request,"account/credit_card_delete.html",context)
