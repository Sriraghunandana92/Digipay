from django.shortcuts import render,redirect
from bankaccounts.models import Account,KYC
from django.db.models import Q
from transaction.models import Transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal 

def user_request_payment(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    if query:
        account = account.filter(
            Q(account_number = query)
        ).distinct()
    context = {
            'account' : account,
            'query' : query
        }
    return render(request,"payment_request/user_request_payment.html",context)



def request_amount(request,account_number):
    account=Account.objects.get(account_number=account_number)
    sender=request.user
    receiver=account.user
    sender_account=request.user.account
    receiver_account=account
    
    if request.method =='POST':
        amount=request.POST.get('amount-send')
        description=request.POST.get('description')
        print(amount)
        print(description)
        if sender_account.account_balance > 0 and amount:
            new_transaction=Transaction.objects.create(
                description=description,
                user=request.user,
                amount=amount,
                sender_account=sender_account,
                sender=sender,
                receiver=receiver,
                receiver_account=receiver_account,
                status='request_sent',
                transaction_type='request',
            )
            new_transaction.save()
            transaction_id=new_transaction.transaction_id
            return  redirect('transactions:request_amount_confirmation',account.account_number,transaction_id)
    return render(request,'payment_request/request_amount.html',{'account':account})

def request_amount_confirmation(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        'account' : account,
        'transaction' : transaction
    }
    return render (request,'payment_request/request_amount_confirmation.html',context)


def request_amount_final_process(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == account.pin_number:
            transaction.status = "request_sent"
            transaction.save()
            messages.success(request, "Your payment request have been sent successfully.")
            return redirect("transactions:request_confirmation_success", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "An Error Occured, try again later.")
        return redirect("bankaccounts:dashboard")

def request_confirmation_success(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/request_confirmation_success.html", context)


def send_confirmation(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/send_confirmation.html", context)

def send_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user 
    sender_account = request.user.account 

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Insufficient Funds, fund your account and try again.")
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(request, f"Settled to {account.user.kyc.full_name} was successfull.")
                return redirect("send-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:send-confirmation", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error Occured")
        return redirect("account:dashboard")
    
def SendCompleted(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
                "account":account,
                "transaction":transaction,
            }
    return render(request, "payment_request/SendCompleted.html", context)
