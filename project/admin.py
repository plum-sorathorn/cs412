from django.contrib import admin
from .models import CuisineType, UserRestaurantEntry, Review

# Register your models here.

admin.site.register(CuisineType)
admin.site.register(UserRestaurantEntry)
admin.site.register(Review)