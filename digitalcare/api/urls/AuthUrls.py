from django.urls import path
from api.views import (RegisterView, LoginView, OTPVerificationView, ResendOTPView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'), 
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    
]