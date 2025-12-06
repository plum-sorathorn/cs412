# File: serializers.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 12/05/2025
# Description: serializers for the backend API (project)

from rest_framework import serializers
from .models import CuisineType, UserRestaurantEntry, Review

# Cuisine Type Serializer
class CuisineTypeSerializer(serializers.ModelSerializer):
    ''' accepted fields for cuisine types '''
    class Meta:
        model = CuisineType
        fields = ('id', 'name', 'description')

# Review Serializer (nested)
class ReviewSerializer(serializers.ModelSerializer):
    ''' accepted fields for reviews '''
    class Meta:
        model = Review
        # We only need rating and comment for the history
        fields = ('rating', 'comment', 'date_posted') 

# User History Entry Serializer
class UserRestaurantEntrySerializer(serializers.ModelSerializer):
    ''' accepted for a restaurant entry '''
    cuisine_name = serializers.CharField(source='cuisine.name', read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = UserRestaurantEntry
        fields = (
            'id', 
            'name', 
            'address', 
            'date_picked',
            'external_api_id', 
            'cuisine',         # The ID of the cuisine type
            'cuisine_name',    # The name of the cuisine for display
            'reviews',         # Nested reviews
        )
        read_only_fields = ('user',)

    def get_reviews(self, obj):
        # Simple method to get reviews for the read-only list
        reviews = obj.review_set.all()
        return [{'rating': r.rating, 'comment': r.comment, 'date': r.date_posted} for r in reviews]

# Serializer to process incoming data for login
class LoginDataSerializer(serializers.Serializer): 
    ''' authenticate username and password for login '''
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

# Serializer to process incoming data for registration
class RegisterDataSerializer(serializers.Serializer):
    ''' fields required for new user registration '''
    username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

# Serializer to return the authentication token
class TokenSerializer(serializers.Serializer):
    ''' return a auth token for logged-in use '''
    token = serializers.CharField(max_length=40)