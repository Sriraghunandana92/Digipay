from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User
from bankaccounts.models import Account,KYC

TRANSACTION_STATUS = (
    ['FAILED','failed'],
    ['COMPLETED','completed'],
    ['PENDING','processing'],
    ['REQUEST_SENT','request_sent'],
    ['REQUEST_PROCESSING','request_processing']
)

TRANSACTION_TYPE = (
    ['transfer','TRANSFER'],
    ['withdraw','WITHDRAW'],
    ['refund','REFUND'],
    ['received','RECEIVED'],
    ['request','REQUEST'],
    ['none','NONE']
)
CARD_TYPE = (
    ['MASTER','master'],
    ['VISA','visa'],
    ['RUPAY','rupay'],
    ['PLATINUM','platinum']
)
card_status = (
    ['ACTIVE','active'],
    ['DEACTIVE','deactive']
)

# Create your models here.
class Transaction(models.Model):
    transaction_id =ShortUUIDField(unique=True,length=12,max_length=25,prefix='DIPY')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    amount = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    description = models.CharField(max_length=200,blank=True,null=True)
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,max_length=200,related_name='receiver')
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,max_length=200,related_name='sender')
    receiver_account = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,max_length=200,related_name='received_amount')
    sender_account = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,max_length=200,related_name='sender_amount')
    status = models.CharField(max_length=200,choices=TRANSACTION_STATUS,default='pending')
    transaction_type = models.CharField(max_length=200,choices=TRANSACTION_TYPE,default=None)
    date  = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return f"{self.user}"

class CreditCard(models.Model):
    card_id = ShortUUIDField(unique=True,length=10,max_length=20,prefix='CRED',alphabet="123456789")
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)
    number = ShortUUIDField(unique=True,length=12,max_length = 16,prefix='CCNO')
    month = models.CharField(max_length=15)
    year = models.IntegerField()
    CVV = ShortUUIDField(unique=True,length=3,max_length=6,alphabet="123456789")
    card_type = models.CharField(max_length=50,choices=CARD_TYPE)
    card_status = models.CharField(max_length=200,choices=card_status)
    date = models.DateField(auto_now_add=True)
    
    

    def __str__(self):
        return f"{self.user}"