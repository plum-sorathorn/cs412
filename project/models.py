# File: models.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/24/2025
# Description: contains the data models of the final project

from django.db import models

# instead of having our own User model, we'll use Django's
from django.contrib.auth.models import User

class CuisineType(models.Model):
    ''' Used to define and categorize food types (for filtering) '''
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserRestaurantEntry(models.Model):
    ''' A record of a restaurant the user picked and visited '''
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(CuisineType, on_delete=models.SET_NULL, null=True)

    # Data fields
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    date_picked = models.DateField()
    external_api_id = models.TextField(blank=True) # to store the restaurant's id from the map API
    
    def __str__(self):
        return f"{self.name} | {self.cuisine} | at {self.address}"

class Review(models.Model):
    ''' Captures the user's detailed feedback for an entry '''
    entry = models.ForeignKey(UserRestaurantEntry, on_delete=models.CASCADE)
    
    rating = models.TextField(blank=True) # Will be 1 to 5
    comment = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.entry.name} | Rating: {self.rating}"