from django.contrib import admin
from transaction.models import Transaction,CreditCard

# Register your models here.
admin.site.register(Transaction)


class CredictCardAdmin(admin.ModelAdmin):
    list_display = ('user','name','number','month','year','card_type','card_status')

admin.site.register(CreditCard,CredictCardAdmin)