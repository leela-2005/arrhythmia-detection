from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]
