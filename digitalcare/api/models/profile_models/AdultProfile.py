from django.db import models
from .PatientProfile import PatientProfile
from ..authentication_models import User

class AdultProfile(PatientProfile):
    """Additional info for adult patients (staff, faculty, etc.)"""
    
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Adult-specific info
    spouse_partner_name = models.CharField(max_length=100, blank=True)
    spouse_partner_phone = models.CharField(max_length=15, blank=True)
