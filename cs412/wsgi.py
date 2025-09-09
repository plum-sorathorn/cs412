# File: wsgi.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/2/2025
# Description: default django file for configurations

"""
WSGI config for cs412 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')

application = get_wsgi_application()
