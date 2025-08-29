from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(days=365 * 3)