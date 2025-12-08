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

class RestaurantFilterSerializer(serializers.Serializer):
    ''' Serializer to handle the list of restaurants sent from Frontend for filtering '''
    # We receive a list of Place IDs (strings)
    place_ids = serializers.ListField(child=serializers.CharField())
    # Mode: 'new' or 'favorites'
    filter_mode = serializers.ChoiceField(choices=['new', 'favorites'])

class CuisineFilterSerializer(serializers.Serializer):
    ''' Serializer to handle the list of Cuisine Types sent from Frontend for suggestions '''
    # We receive a list of types available in the current map view (e.g., ['italian', 'thai'])
    available_types = serializers.ListField(child=serializers.CharField())
    # Mode: 'new_types' or 'tried_types'
    filter_mode = serializers.ChoiceField(choices=['new_types', 'tried_types'])

class LogVisitSerializer(serializers.Serializer):
    ''' Serializer for logging a visit (Let's Eat button) '''
    name = serializers.CharField()
    address = serializers.CharField()
    external_api_id = serializers.CharField()
    cuisine_type = serializers.CharField()

class ReviewSubmissionSerializer(serializers.Serializer):
    ''' Validates data for creating/updating a review '''
    entry_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True)