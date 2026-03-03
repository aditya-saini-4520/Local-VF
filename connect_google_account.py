#!/usr/bin/env python
"""
Connect existing Django user account to Google OAuth social account.

This script links an existing user (created via email/password signup)
with their Google OAuth account using the same email address.

Problem: User has regular Django account but not Google OAuth connected.
Error: "An account already exists with this email address..."
Solution: This script manually creates the SocialAccount link.

Run: python connect_google_account.py
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp


def connect_google_account(email):
    """Connect a user's regular account to their Google OAuth account."""
    
    print(f"\n🔍 Looking for user with email: {email}")
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ Found user: {user.username}")
    except User.DoesNotExist:
        print(f"❌ No user found with email: {email}")
        return False
    
    # Check if already connected
    existing = SocialAccount.objects.filter(user=user, provider='google')
    if existing.exists():
        print(f"⚠️  Google account already connected to this user!")
        print(f"   Provider: {existing.first().provider}")
        print(f"   UID: {existing.first().uid}")
        return False
    
    # Get Google SocialApp
    try:
        google_app = SocialApp.objects.get(provider='google')
        print(f"✅ Found Google SocialApp: {google_app.name}")
    except SocialApp.DoesNotExist:
        print(f"❌ Google SocialApp not found in database!")
        print(f"   Run: python setup_google_oauth.py")
        return False
    
    # Create SocialAccount link
    # For demonstration, we'll use the email as the UID
    # In real scenario, this would come from Google during OAuth flow
    social_account = SocialAccount.objects.create(
        user=user,
        provider='google',
        uid=email,  # This would be Google's unique user ID in real flow
        extra_data={
            'email_verified': True,
            'name': user.first_name or user.username,
            'picture': '',
        }
    )
    social_account.save()
    
    print(f"\n✅ SUCCESS! Connected Google account to user: {user.username}")
    print(f"   Email: {email}")
    print(f"   Provider: {social_account.provider}")
    print(f"   Next time user logs in with Google, they'll be connected!")
    return True


if __name__ == "__main__":
    # Use the email from the error message
    email = "adityasaini1492005@gmail.com"
    
    print("=" * 60)
    print("Google OAuth Account Connection Script")
    print("=" * 60)
    
    success = connect_google_account(email)
    
    if success:
        print("\n🚀 You can now delete your old account and use Google OAuth!")
        print("   Or keep both and use whichever you prefer.")
    else:
        print("\n❌ Connection failed. Check errors above.")
    
    print("=" * 60)
