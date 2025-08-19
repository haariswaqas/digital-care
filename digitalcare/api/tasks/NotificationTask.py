from celery import shared_task
from ..models import Notification, User

@shared_task
def create_notification_task(user_id, message):
    
    try:
        user = User.objects.get(id=user_id)
        Notification.objects.create(recipient=user, message=message)
        print(f"Notification created for user {user_id}")
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist")

