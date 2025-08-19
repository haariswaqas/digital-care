from ..models import User, Otp
from ..tasks import send_email_task
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.signing import Signer
import urllib.parse
import sys

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    # Avoid sending emails during migrations
    if any(cmd in sys.argv for cmd in ['makemigrations', 'migrate']):
        return

    if created and not instance.is_superuser:
        try:
            # Self-registration: generate and send OTP
            otp_obj, otp_created = Otp.objects.get_or_create(user=instance)
            if otp_created or not otp_obj.is_verified:
                otp_code = Otp.generate_otp()
                otp_obj.code = otp_code
                otp_obj.save()

                subject = "Welcome to the Digital Care Portal! Verify Your Email!"
                message = (
                    f"Dear {instance.username},\n\n"
                    "Welcome! Before you can log in, please verify your email address.\n\n"
                    f"Your OTP is: {otp_code}\n\n"
                    "Best regards,\nHospital Admin"
                )
                
                # Use try-except for the email task
                try:
                    send_email_task.delay(subject, message, [instance.email])
                except Exception as e:
                    # Log the error but don't fail the registration
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send welcome email: {str(e)}")
                    
        except Exception as e:
            # Log any errors in OTP creation but don't fail registration
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in send_welcome_email signal: {str(e)}")