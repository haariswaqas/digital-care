from django.db import models
from .PatientProfile import PatientProfile
from ..authentication_models import User

class VisitorProfile(PatientProfile):
    """Additional info for visitor patients"""
   
    visiting_purpose = models.CharField(max_length=200, null=True, blank=True)
    host_contact_name = models.CharField(max_length=100, null=True, blank=True)
    host_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    expected_stay_duration = models.CharField(max_length=50, null=True, blank=True)
    
    # Visitor-specific considerations
    home_address = models.TextField(null=True, blank=True)
    local_accommodation = models.CharField(max_length=200, null=True, blank=True)