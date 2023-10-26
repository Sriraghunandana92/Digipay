from django.shortcuts import render,redirect
from bankaccounts.models import Account,KYC
from django.db.models import Q
from transaction.models import Transaction
from django.contrib import messages
# Create your views here.

def search_user_by_account_number(request):
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

    return render(request,'transaction/amount_transfer.html',context)


def amount_transfer(request,account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request,"Account doesn't exit")
        return redirect('search')
    
    context = {
        'account' :account
    }
    return render(request,"transaction/transaction_confirmation.html",context)

def Amount_transfer_process(request,account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    receiver = account.user
    sender_account = request.user.account
    receiver_account = account
    if request.method == 'POST':
        amount = request.POST.get('amount-send')
        description = request.POST.get('description')


        if sender_account.account_balance > 0 and amount:
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                sender_account = sender_account,
                sender = sender,
                receiver = receiver,
                receiver_account = receiver_account,
                status = 'processing',
                transaction_type =  "None"
            )
            new_transaction.save()
            transaction_id = new_transaction.transaction_id
            return redirect ("transaction_confirmation",account.account_number,transaction_id)
        else:
            messages.warning(request,"Insufficient Fund")
            return redirect("amount_transfer",account.account_number)
            
    
    return render(request,"transaction/amount-transfer-process.html",{})




def transaction_confirmation(request,account_number,transaction_id):
    account = Account.objects.get(account_number = account_number)
    transaction  = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        'account':account,
        'transaction' : transaction,
    }
    return render(request,'transaction/transaction_confirmation.html',context)

def transfer_process(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    sender_account = request.user.account

    if request.method == 'POST':
        pin_number = request.POST.get('pin-number')
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = 'Completed'
            transaction.save()
            print(sender_account.account_balance)
            print(transaction.amount)

            sender_account.account_balance -=transaction.amount
            sender_account.save()
            print(sender_account.account_balance)

            messages.success(request,"transaction complete")
            return redirect("transactions:transfer-completed",account.account_number,transaction.transaction_id)
        else:
            messages.warning(request,"Incorect pin")
            return redirect('transactions:transaction_confirmation',account.account_number,transaction.transaction_id)
    else:
        return redirect(request,"transactions:transaction_confirmation",account.account_number,transaction.transaction_id)

def transfer_completed(request,account_number,transaction_id):
    account = Account.objects.get(account_number = account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        'account':account,
        'transaction' : transaction,
    }
    return render(request,"transaction/transfer-completed.html",context)


def transaction_details(request,transaction_id):
    user=request.user
    account = Account.objects.get(user=user) 
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    reciever = account.user
    context = {
        'account':account,
        'transaction':transaction,
        'reciever':reciever,  
    }
    return render(request,'transaction/transactions_details.html',context)
