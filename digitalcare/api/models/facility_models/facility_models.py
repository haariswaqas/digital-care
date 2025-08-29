# api/models/facility.py
from django.db import models
from ..authentication_models import User
class Facility(models.Model):
    CLINIC = 'clinic'
    PHARMACY = 'pharmacy'
    TYPE_CHOICES = [(CLINIC, 'Clinic'), (PHARMACY, 'Pharmacy')]
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name="facility", null=True, blank=True)
    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_partner = models.BooleanField(default=True)  # partner clinics/pharmacies
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name})"
