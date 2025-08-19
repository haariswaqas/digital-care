from django.db import models 
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string
from .User import User


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.code}"

    def is_expired(self):
        # OTP expires after 10 minutes (adjust as needed)
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() > expiry_time

    @staticmethod
    def generate_otp():
        # Generate a 6-digit OTP code
        return ''.join(random.choices(string.digits, k=6))
