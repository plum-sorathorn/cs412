# File: apps.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 10/29/2025
# Description: app configurations file for voter_analytics

from django.apps import AppConfig


class VoterAnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "voter_analytics"
