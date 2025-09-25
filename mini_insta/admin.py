# File: admin.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: admin access file for mini_insta

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)