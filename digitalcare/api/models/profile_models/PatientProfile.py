# api/models/patient_profile.py
from django.db import models
from ..authentication_models import User



class PatientProfile(models.Model):
    """Base patient profile with common medical information"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Basic medical info common to all patients
    BLOOD_GROUPS = [
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
    ]
    nhis_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True, help_text="Known allergies")
    chronic_conditions = models.TextField(null=True, blank=True, help_text="Ongoing medical conditions")
    current_medications = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Location info for nearby provider search
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Insurance/Payment info
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_policy_number = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Patient Profile - {self.first_name}"


