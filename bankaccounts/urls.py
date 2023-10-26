from django.urls import path
from bankaccounts import views

app_name = 'bankaccounts'

urlpatterns = [
    path('',views.kyc_reg,name='kyc'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('account/',views.account,name='account'),
    path('dashboard/',views.dashboard,name='dashboard')
]