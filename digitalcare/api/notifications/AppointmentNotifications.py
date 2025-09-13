# api/signals/appointment_notifications.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Appointment
from ..tasks import create_notification_task

# 1️⃣ Notify the doctor when a patient books a new appointment
@receiver(post_save, sender=Appointment)
def notify_doctor_on_booking(sender, instance, created, **kwargs):
    if created and instance.doctor:
        doctor_user = instance.doctor.user
        message = (
            f"New appointment booked by patient {instance.patient.get_full_name()} "
            f"for {instance.scheduled_at} at {instance.facility.name}."
        )
        create_notification_task.delay(user_id=doctor_user.id, message=message)

# 2️⃣ Notify the patient when the doctor confirms or cancels the appointment
@receiver(post_save, sender=Appointment)
def notify_patient_on_status_change(sender, instance, created, **kwargs):
    if not created and instance.status in [Appointment.CONFIRMED, Appointment.CANCELLED]:
        patient = instance.patient
        message = f"Your appointment scheduled at {instance.scheduled_at} has been {instance.status}."
        create_notification_task.delay(user_id=patient.id, message=message)
