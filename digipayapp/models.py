from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_form(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    phone = models.BigIntegerField()
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200)


class user_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    #additional fields
    user_url = models.URLField(blank=True)
    user_img = models.ImageField(upload_to="userimage",blank=True)
    
    