# In api/models/health_card.py or a separate signals.py file

from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import User, HealthCard

@receiver(post_save, sender=User)
def create_health_card(sender, instance, created, **kwargs):
    """Automatically create a HealthCard when a new User is created"""
    if created:  # Only for newly created users
        HealthCard.objects.create(
            user=instance,
            card_type=HealthCard.CardType.SMART  # Default to SMART card
        )

# Optional: Also handle user updates
@receiver(post_save, sender=User)
def save_health_card(sender, instance, **kwargs):
    """Ensure the health card is saved when user is updated"""
    if hasattr(instance, 'health_card'):
        instance.health_card.save()