from django.urls import path
from api.views import (PasswordResetRequestView, PasswordResetConfirmView)

urlpatterns = [
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]