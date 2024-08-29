from django.urls import path
from .views import CustomLogoutView
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('home1/', views.home1, name='home1'),
    path('otp/<str:uid>/', views.otpVerify, name='otp'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('verify_email_otp/', views.verify_email_otp, name='verify_email_otp'),
    path('logout/', CustomLogoutView.as_view(), name='account_logout'),
]
