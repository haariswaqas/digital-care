from django.db import models
from .PatientProfile import PatientProfile
from ..authentication_models import User

class StudentProfile(PatientProfile):
    """Additional info specific to student patients"""
    
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    program_of_study = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)
    hall = models.CharField(max_length=50, blank=True, null=True)
    
    # Student-specific medical considerations
    parent_guardian_name = models.CharField(max_length=255, null=True, blank=True)
    parent_guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    