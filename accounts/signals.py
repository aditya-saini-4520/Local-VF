from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth.models import User

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile for newly created users.
    Defaults to 'customer' role.
    """
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={"role": UserProfile.Roles.CUSTOMER}
        )


@receiver(social_account_added)
def create_profile_on_social_login(sender, request, sociallogin, **kwargs):
    """
    Signal handler for post-social-login.
    Creates a UserProfile with role=customer if one doesn't exist.
    """
    user = sociallogin.user
    UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": UserProfile.Roles.CUSTOMER}
    )
