from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from notifications.models import Notification


@receiver(post_save, sender=Review)
def create_review_notification(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification for the vendor owner
    whenever a new review is created for their vendor.
    """
    if created:
        vendor = instance.vendor
        customer = instance.customer
        
        # Get the vendor owner
        if vendor.owner:
            message = f"New review ({instance.rating} stars) from {customer.first_name or customer.username}: {instance.comment[:50] if instance.comment else 'No comment'}"
            
            Notification.objects.create(
                user=vendor.owner,
                message=message,
                is_read=False
            )
