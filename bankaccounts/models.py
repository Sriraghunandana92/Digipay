from django.db import models
import uuid
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save


# Create your models here.
ACCOUNT_STATUS = (
    ['in_active','IN_ACTIVE'],
    ['active','ACTIVE']
)


MARITAL_STATUS = (
    ['single','SINGLE'],
    ['married','MARRIED'],
    ['others','OTHERS']
)


GENDER = (
    ['male','MALE'],
    ['female','FEMALE'],
    ['others',"OTHERS"]
)

IDENTITY_TYPE = (
    ['pan_card','PANCARD'],
    ['aadhar','AADHAR'],
    ['passport','PASSPORT'],
    ['driving_liscence','DRIVING_LISCENCE'],
    ['others','OTHERS']

)
class Account(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    account_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)

    account_number = ShortUUIDField(unique=True,length=12,max_length=25,prefix='217',alphabet='1234567890')

    account_id = ShortUUIDField(unique=True,length=10,max_length=25,prefix='DIGP',alphabet='1234567890')

    pin_number = ShortUUIDField(unique=True,length=4,max_length=7,alphabet='1234567890')

    account_status = models.CharField(max_length=100,choices=ACCOUNT_STATUS, default='in-active')
    
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class KYC(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    image = models.ImageField(upload_to="kyc/")
    marital_status = models.CharField(max_length=200,choices=MARITAL_STATUS)
    gender = models.CharField(max_length=100,choices=GENDER)
    identity_type = models.CharField(max_length=200,choices=IDENTITY_TYPE)
    inentify_image = models.ImageField(upload_to='kyc/')
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc/")

    #address
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    

    #contact
    phone = models.CharField(max_length=100)
    email = models.EmailField(unique=True,blank=True)

    
def create_account(sender,instance,created,**kwargs):
    if created :
        Account.objects.create(user=instance)

def save_account(sender,instance,**kwargs):
    instance.account.save()

post_save.connect(create_account,sender=User)
post_save.connect(save_account,sender=User)
