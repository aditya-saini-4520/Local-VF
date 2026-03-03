from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to auto-populate form fields and skip unnecessary steps
    for Google OAuth users.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Auto-populate email from social account data
        """
        if sociallogin.is_existing:
            return

        try:
            if 'email' in sociallogin.account.extra_data:
                sociallogin.user.email = sociallogin.account.extra_data['email']
        except AttributeError:
            pass

    def populate_user(self, request, sociallogin, data):
        """
        Populate user data from social provider
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Use email prefix as username to avoid username requirement
        if data.get('email'):
            username = data['email'].split('@')[0]
            user.username = username
        
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow auto signup for social accounts
        """
        return True
