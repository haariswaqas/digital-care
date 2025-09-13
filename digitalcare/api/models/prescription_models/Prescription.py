# api/models/prescription.py
from django.db import models
from ..appointment_models import Consultation


class Prescription(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)     
    frequency = models.CharField(max_length=100)   
    duration = models.CharField(max_length=100)     
    instructions = models.TextField(blank=True)     
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} for {self.consultation.appointment.patient}"
