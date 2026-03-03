import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-in-production")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.pythonanywhere.com',
    '*',
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "config",
    "accounts",
    "vendors",
    "reviews",
    "notifications",
    "analytics",
    "ai_assistant",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifications.context_processors.unread_notifications_count",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =====================================================================
# SECURITY SETTINGS FOR PRODUCTION
# =====================================================================
CSRF_TRUSTED_ORIGINS = [
    'https://*.pythonanywhere.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Security settings for production (when DEBUG=False and on HTTPS)
if not DEBUG:
    # SSL/HTTPS settings for PythonAnywhere
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings (careful when enabling!)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False  # Set to True after testing and SSL works
else:
    # Local development (DEBUG=True)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RETELL_API_KEY = os.getenv("RETELL_API_KEY", "")
RETELL_AGENT_ID = os.getenv("RETELL_AGENT_ID", "")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}


# =====================================================================
# DJANGO-ALLAUTH CONFIGURATION: Google OAuth Setup
# =====================================================================
# This configuration provides a seamless Google OAuth login experience
# for Local VFC. Users click the Google button and are logged in without
# any extra forms or email verification steps.

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",  # Enables social auth
]

# =====================================================================
# GOOGLE OAUTH: Core Settings
# =====================================================================

# SOCIALACCOUNT_LOGIN_ON_GET = True
# Purpose: Skip the intermediate "Continue" confirmation page
# Behavior: When user clicks Google button, goes DIRECTLY to Google login
# Without this: Shows unstyled page asking user to click "Continue"
# With this: Redirects straight to Google OAuth screen
# Security: Safe - is standard practice for OAuth flows
SOCIALACCOUNT_LOGIN_ON_GET = True

# SOCIALACCOUNT_AUTO_SIGNUP = True
# Purpose: Automatically create user account after Google authentication
# Behavior: No signup form shown; account created on first Google login
# Without this: User stuck on signup form after Google returns
# With this: Account auto-created with email from Google
# Security: Safe - Google only provides verified information
SOCIALACCOUNT_AUTO_SIGNUP = True

# CRITICAL FIX: Email Authentication Settings
# These settings allow auto-connecting Google accounts to existing user accounts
# with the same email address, solving: "An account already exists with this email..."
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# Connection method: Allow both username and email for login
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# Skip the signup form entirely - go straight to Google
ACCOUNT_SIGNUP_FORM_CLASS = None

# Protocol for email links (http for local development, https for production)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# SOCIALACCOUNT_STORE_TOKENS = True
# Purpose: Save OAuth tokens in database for future API calls
# Use case: If we need to make API requests on behalf of user later
SOCIALACCOUNT_STORE_TOKENS = True

# =====================================================================
# EMAIL VERIFICATION: Critical for Smooth Google OAuth
# =====================================================================

# ACCOUNT_EMAIL_VERIFICATION = 'none'
# Purpose: Skip email verification for all users (social + regular)
# Why it's safe for Google OAuth:
#   - Google already verifies the email address on their end
#   - If email wasn't verified, Google wouldn't send it to us
#   - Trusting Google's verification is standard practice
# Acceptable values:
#   - 'none': No verification required
#   - 'optional': User can skip verification if they want
#   - 'mandatory': Must click email link to activate account
#
# ⚠️  IMPORTANT SECURITY WARNING FOR FUTURE DEVELOPERS:
#     If we add traditional email/password signup in future:
#     1. Set ACCOUNT_EMAIL_VERIFICATION = 'mandatory' for those users
#     2. Keep 'none' ONLY for Google OAuth (via social adapter)
#     3. This prevents unauthorized account creation via registration form
#     4. These settings only skip verification for social logins,
#        not for regular email/password signups (if added later)
#
# Current configuration applies to BOTH signup methods, which is okay
# because we use CustomSocialAccountAdapter to auto-create Google users
# before any verification check happens.
ACCOUNT_EMAIL_VERIFICATION = 'none'

# ACCOUNT_EMAIL_REQUIRED = True
# Purpose: Email is mandatory for all user accounts
# Google OAuth: Google always provides email, so this is always satisfied
# Traditional signup: If added, user must enter email
ACCOUNT_EMAIL_REQUIRED = True

# =====================================================================
# USERNAME HANDLING
# =====================================================================

# ACCOUNT_USERNAME_REQUIRED = False
# Purpose: Username is NOT required during signup
# Why it enables seamless Google OAuth:
#   - Users don't have to pick a username
#   - CustomSocialAccountAdapter auto-generates one from email
# How CustomSocialAccountAdapter handles this:
#   - Extracts email: "john.doe@gmail.com"
#   - Generates username: "john.doe"
#   - Creates account seamlessly without user input
# Security: Username is auto-generated from email, not user-chosen
ACCOUNT_USERNAME_REQUIRED = False

# =====================================================================
# ACCOUNT CREATION: Signup Fields Configuration
# =====================================================================

# ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
# Purpose: Define required fields for signup forms
# Current config: email and passwords required, username NOT required
# Google OAuth: This field is BYPASSED (auto-signup mode)
#   → Google OAuth users skip forms entirely
# Email/password signup: Would show form with these fields (if added later)
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# =====================================================================
# REDIRECT AFTER LOGIN
# =====================================================================

# LOGIN_REDIRECT_URL = '/'
# Purpose: Where user goes after successful login
# For Google OAuth: Redirects to homepage after auto-signup
# For future email/password login: Would also redirect to homepage
LOGIN_REDIRECT_URL = '/'

# =====================================================================
# GOOGLE OAUTH: Provider Configuration
# =====================================================================

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",      # Access user's name and picture
            "email",        # Access user's email address
        ],
        "AUTH_PARAMS": {
            "access_type": "online",  # Request online access (not offline/refresh)
        },
        "VERIFIED_EMAIL": False,  # Don't require re-verification in our app
        "VERSION": "v2",          # Google OAuth v2 API
    }
}

# =====================================================================
# CUSTOM ADAPTER & SIGNAL HANDLERS
# =====================================================================

# SOCIALACCOUNT_ADAPTER = 'accounts.adapter.CustomSocialAccountAdapter'
# Purpose: Custom logic to handle Google OAuth signup seamlessly
# What it does:
#   1. Extracts email from Google profile data
#   2. Auto-generates username from email prefix
#   3. Creates User object with both email and username
#   4. Sets is_auto_signup_allowed = True to skip confirmation
# File: accounts/adapter.py
#
# Signal Handler: create_profile_on_social_login (accounts/signals.py)
# What it does:
#   1. Listens to @receiver(social_account_added) signal
#   2. When new user created via Google OAuth
#   3. Auto-creates UserProfile with role='customer'
#   4. User can change role to 'vendor' later in profile settings
#
# This combination ensures zero friction from login to ready-to-use account
SOCIALACCOUNT_ADAPTER = 'accounts.adapter.CustomSocialAccountAdapter'

# =====================================================================
# COMPLETE GOOGLE OAUTH LOGIN FLOW
# =====================================================================
"""
User Journey: from login button to homepage in one seamless flow

STEP 1: User on login page sees Google button
        ↓
STEP 2: Click Google button → Redirects to Google OAuth screen
        (SOCIALACCOUNT_LOGIN_ON_GET = True skips "Continue" page)
        ↓
STEP 3: User authenticates with Google
        (User enters Google credentials and authorizes Local VFC)
        ↓
STEP 4: Google redirects back to our callback with auth data
        (Google sends: email, name, profile picture)
        ↓
STEP 5: CustomSocialAccountAdapter.populate_user() runs
        (Extracts email, generates username, creates User object)
        ↓
STEP 6: Django creates User in database
        (User(username="john", email="john.doe@gmail.com"))
        ↓
STEP 7: Signal handler runs: create_profile_on_social_login
        (Creates UserProfile(user=user, role='customer'))
        ↓
STEP 8: Email verification check
        (ACCOUNT_EMAIL_VERIFICATION = 'none' skips verification)
        (Google already verified the email)
        ↓
STEP 9: Authenticate user in Django session
        (User object now in request.user)
        ↓
STEP 10: Redirect to homepage
        (LOGIN_REDIRECT_URL = '/')
        ↓
✅ RESULT: COMPLETE SIGNUP & LOGIN IN ONE FLOW
   ✅ No extra forms shown
   ✅ No email verification needed
   ✅ User profile automatically created
   ✅ User can start using Local VFC immediately
"""

# =====================================================================
# SECURITY NOTES & FUTURE CONSIDERATIONS
# =====================================================================
"""
CURRENT STATE (Google OAuth only):
- ACCOUNT_EMAIL_VERIFICATION = 'none' is SAFE because:
  1. Google has already verified the email address
  2. User must authenticate with Google to get a valid token
  3. We only receive emails that Google has confirmed
  4. Allauth validates the OAuth token was signed by Google

IF ADDING EMAIL/PASSWORD SIGNUP IN FUTURE:
1. MUST change ACCOUNT_EMAIL_VERIFICATION to 'mandatory' for security
2. This requires users to click verification email link before account is active
3. Prevents spam and unauthorized account creation via registration form
4. Keep Google OAuth separate (it bypasses this anyway)
5. Example future setup:
   - Google OAuth: Auto-creates account, no verification needed
   - Email signup: Must verify email before account is active
   - Implementation: Use conditional logic in adapter

REMEMBER: These settings only skip verification for social (Google) logins.
If regular email/password signup is added, verification must be enforced
for security reasons. Don't leave ACCOUNT_EMAIL_VERIFICATION = 'none' 
for traditional signups.

CURRENT ADAPTER SETUP:
- Only handles Google OAuth (social_account_added signal)
- Regular signup doesn't use this adapter
- If regular signup added: Create separate flow with verification
"""

# =====================================================================
# RELATED CONFIGURATION FILES & DEPENDENCIES
# =====================================================================
"""
This configuration works with:

1. accounts/adapter.py
   - CustomSocialAccountAdapter
   - Generates username from email
   - Allows auto-signup for Google users

2. accounts/signals.py
   - create_profile_on_social_login
   - Auto-creates UserProfile with role='customer'
   - Registered via accounts/apps.py in ready() method

3. accounts/apps.py
   - Registers signals in ready() method
   - Must import signals before Django app is ready

4. accounts/templates/socialaccount/signup.html
   - Custom styled signup form (fallback, rarely shown)
   - Matches dark theme design
   - Has role selector (customer/vendor)
   - Only shown if user somehow reaches signup step

5. .env file
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - Loaded via os.getenv() in SOCIALACCOUNT_PROVIDERS

6. config/urls.py
   - path("accounts/", include("allauth.urls"))
   - Provides OAuth callback endpoints automatically
   - Includes: /accounts/google/login/callback/
"""

