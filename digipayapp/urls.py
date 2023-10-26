from digipayapp import views
from django.urls import path

app_name = 'digipayapp'

urlpatterns = [
    path('',views.reg,name='reg'),
    path('signin/',views.signin,name='signin'),
    # path('user_logout',views.user_logout,name='user_logout'),
  
]