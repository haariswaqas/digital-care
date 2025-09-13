# api/models/symptom.py
from django.db import models
from .Appointment import Appointment

class Symptom(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='symptoms')
    description = models.TextField()
    image = models.ImageField(upload_to='symptom_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Symptom {self.id} for Appointment {self.appointment.id}"
