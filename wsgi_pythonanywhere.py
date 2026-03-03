# USE THIS FILE CONTENT FOR PYTHONANYWHERE WSGI CONFIGURATION
# Paste this entire content into your PythonAnywhere WSGI configuration file
# Path in PythonAnywhere: /var/www/yourusername_pythonanywhere_com_wsgi.py

import os
import sys

# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
# Example: /home/aditya/local-vfc/local vfc
path = '/home/yourusername/local-vfc/local vfc'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Get SECRET_KEY from PythonAnywhere environment variables
# Set this in PythonAnywhere Web tab → Environment variables
os.environ.setdefault('SECRET_KEY', 'change-this-to-your-secret-key')
os.environ.setdefault('DEBUG', 'False')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
