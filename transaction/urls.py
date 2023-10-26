from django.urls import path
from transaction import transfer
from transaction import views
from transaction import payment_request,credit_card

app_name = "transactions"

urlpatterns = [
    path('',transfer.search_user_by_account_number,name='search'),
    path('amount_transfer/<account_number>/',transfer.amount_transfer,name = "amount_transfer"),
    path('Amount-transfer-process/<account_number>/',
         transfer.Amount_transfer_process,name='Amount-transfer-process'),
    path('transaction_confirmation/<account_number>/<transaction_id>/',transfer.transaction_confirmation,name='transaction_confirmation'),
    path('transfer_process/<account_number>/<transaction_id>/',transfer.transfer_process,name='transfer_process'),
    path('transfer-completed/<account_number>/<transaction_id>/',transfer.transfer_completed,name='transfer-completed'),
    path('transaction_details/<transaction_id>/',transfer.transaction_details,name="transaction_details"), 


    path('user_request_payment/',payment_request.user_request_payment,name="user_request_payment"),

    
    path('payment_amount/<account_number>/',payment_request.request_amount,name="payment_amount"),
    path('request_amount_confirmation/<account_number>/<transaction_id>/',payment_request.request_amount_confirmation,name="request_amount_confirmation"),
    path('request_confirmation_success/<account_number>/<transaction_id>/',payment_request.request_confirmation_success,name='request_confirmation_success'),
    path('request_amount_final_process/<account_number>/<transaction_id>/,',payment_request.request_amount_final_process,name='request_amount_final_process'),



    path('send_processing/<account_number>/',payment_request.send_processing,name='send_processing'),

    path('send_confirmation/<account_number>/',payment_request.send_confirmation,name = 'send_confirmation'),

    path('SendCompleted/<account_number>/<transaction_id>/',payment_request.SendCompleted,name='SendCompleted'),

    path('credit_card/<number>/',credit_card.credit_card,name='credit_card'),
    path('credit_card_bill/<card_id>/',credit_card.credit_card_bill,name="credit_card_bill"),

    path('withdraw_amount/<card_id>/',credit_card.withdraw_amount,name='withdraw_amount'),
    path('credit_card_delete/<card_id>/',credit_card.credit_card_delete,name="credit_card_delete")
]