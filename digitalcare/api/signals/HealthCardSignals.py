from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import User, HealthCard

# Roles eligible for HealthCard
CARD_ELIGIBLE_ROLES = [User.STUDENT, User.ADULT, User.VISITOR]

@receiver(post_save, sender=User)
def create_health_card(sender, instance, created, **kwargs):
    """Automatically create a HealthCard for eligible users only."""
    if created and instance.role in CARD_ELIGIBLE_ROLES:
        HealthCard.objects.create(
            user=instance,
            card_type=HealthCard.CardType.SMART  # Default to SMART card
        )

@receiver(post_save, sender=User)
def save_health_card(sender, instance, **kwargs):
    """Ensure the health card is saved when the user is updated."""
    if instance.role in CARD_ELIGIBLE_ROLES and hasattr(instance, 'health_card'):
        instance.health_card.save()
