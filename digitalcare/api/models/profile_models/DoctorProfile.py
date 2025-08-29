# api/models/doctor.py
from django.db import models
from ..authentication_models import User
from ..facility_models import Facility

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=150, blank=True)
    clinics = models.ManyToManyField(Facility, related_name='doctors', blank=True)
    is_active = models.BooleanField(default=True)
    license_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
