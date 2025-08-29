# api/models/appointment.py
from django.db import models
from ..facility_models import Facility
from ..profile_models import DoctorProfile
from ..authentication_models import User


class Appointment(models.Model):
    IN_PERSON = 'in_person'
    ONLINE = 'online'
    APPT_TYPES = [(IN_PERSON, 'In-person'), (ONLINE, 'Online')]

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    NO_SHOW = 'no_show'
    STATUS_CHOICES = [(PENDING,'Pending'),(CONFIRMED,'Confirmed'),(CANCELLED,'Cancelled'),(COMPLETED,'Completed'),(NO_SHOW,'No show')]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=APPT_TYPES, default=IN_PERSON)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"Appt {self.id} for {self.patient} at {self.scheduled_at}"
