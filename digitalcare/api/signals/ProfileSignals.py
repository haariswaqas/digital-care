from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import User, VisitorProfile, StudentProfile, AdultProfile, DoctorProfile, Facility

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.STUDENT:
            StudentProfile.objects.create(user=instance)
        elif instance.role == User.VISITOR:
            VisitorProfile.objects.create(user=instance)
        elif instance.role == User.ADULT:
            AdultProfile.objects.create(user=instance)
        elif instance.role == User.DOCTOR:
            DoctorProfile.objects.create(user=instance)
        elif instance.role == User.FACILITY_ADMIN:
            # Create a Facility and link it to this user
            Facility.objects.create(admin=instance, status='Pending')  # You can set other default fields as needed

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == User.STUDENT and hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    elif instance.role == User.VISITOR and hasattr(instance, 'visitorprofile'):
        instance.visitorprofile.save()
    elif instance.role == User.ADULT and hasattr(instance, 'adultprofile'):
        instance.adultprofile.save()
    elif instance.role == User.DOCTOR and hasattr(instance, 'doctorprofile'):
        instance.doctorprofile.save()
    elif instance.role == User.FACILITY_ADMIN and hasattr(instance, 'facility'):
        instance.facility.save()
