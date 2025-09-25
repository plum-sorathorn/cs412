# File: models.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: contains the model of Profile, structure of each user's info

from django.db import models

class Profile(models.Model):
    ''' structure of each user's data attributes '''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.TextField(blank=True)