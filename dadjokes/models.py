# File: models.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: contains models for dadjokes API

from django.db import models

# Create your models here.
class Joke(models.Model):
    ''' structure of each Joke '''
    text = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)

class Picture(models.Model):
    ''' structure of each Picture '''
    image_url = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)