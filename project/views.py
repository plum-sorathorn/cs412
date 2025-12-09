# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/24/2025
# Description: views for backend API (project)

from django.utils import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import CuisineType, UserRestaurantEntry
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .forms import UserRegistrationForm, UserLoginForm
# Fetch all Cuisine Types
class CuisineTypeListView(generics.ListAPIView):
    """ Lists all available cuisine types. """
    queryset = CuisineType.objects.all()
    serializer_class = CuisineTypeSerializer
    # This endpoint is generally public/read-only access
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# Fetch the current User's History
class UserHistoryListView(LoginRequiredMixin, generics.ListAPIView):
    """ Lists all restaurant entries for the authenticated user. """
    serializer_class = UserRestaurantEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserRestaurantEntry.objects.filter(user=self.request.user).order_by('-date_picked')

    def perform_create(self, serializer):
        # Automatically assign the current user when saving
        serializer.save(user=self.request.user)

class DeleteHistoryEntryView(APIView):
    """
    Deletes a specific history entry.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        # Fetch the entry, ensuring it belongs to the current user
        entry = get_object_or_404(UserRestaurantEntry, pk=pk, user=request.user)
        
        # Delete the entry (cascading to reviews)
        entry.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    """ Handles user registration and returns a token upon success. """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use Django form for clean validation and user creation
        form = UserRegistrationForm(data=serializer.validated_data)
        
        if form.is_valid():
            user = form.save()
            # Generate or retrieve the token for the new user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response(TokenSerializer({'token': token.key}).data, status=status.HTTP_201_CREATED)
        
        # If form fails validation (e.g., username already exists)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """ Handles user login and returns the existing token. """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = LoginDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use Django form to authenticate credentials
        form = UserLoginForm(data=serializer.validated_data)

        if form.is_valid():
            user = form.user
            
            # Use Django's login function to set a session 
            login(request, user)
            
            # Retrieve the token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response(TokenSerializer({'token': token.key}).data)
        
        # If authentication fails
        return Response(form.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class RestaurantFilterView(APIView):
    """
    Receives a list of Google Place IDs.
    Returns a filtered list of Place IDs based on User History.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RestaurantFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_ids = serializer.validated_data['place_ids']
        mode = serializer.validated_data['filter_mode']
        user = request.user

        # Get all Place IDs the user has visited
        visited_ids = set(
            UserRestaurantEntry.objects.filter(user=user)
            .values_list('external_api_id', flat=True)
        )

        filtered_ids = []
        if mode == 'new':
            # Keep IDs NOT in history
            filtered_ids = [pid for pid in place_ids if pid not in visited_ids]
        elif mode == 'favorites':
            # Keep IDs found IN history
            filtered_ids = [pid for pid in place_ids if pid in visited_ids]

        return Response({'filtered_ids': filtered_ids})


class CuisineSuggestionView(APIView):
    """
    Receives a list of cuisine types currently on the map.
    Returns a list of types to check/select in the filter modal.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CuisineFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        available_types = serializer.validated_data['available_types']
        mode = serializer.validated_data['filter_mode']
        user = request.user

        # Find cuisines the user has tried
        # We look at the 'api_identifier' of the CuisineType linked to their entries
        tried_types = set(
            UserRestaurantEntry.objects.filter(user=user, cuisine__isnull=False)
            .values_list('cuisine__api_identifier', flat=True)
        )

        suggested_types = []
        if mode == 'new_types':
            # Suggest types NOT in history
            suggested_types = [t for t in available_types if t not in tried_types]
        elif mode == 'tried_types':
            # Suggest types IN history
            suggested_types = [t for t in available_types if t in tried_types]

        return Response({'suggested_types': suggested_types})


class LogVisitView(APIView):
    """
    Logs a restaurant visit. Creates the CuisineType if it doesn't exist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Handle Cuisine Type (Get or Create)
        raw_type = data['cuisine_type']
        pretty_name = raw_type.replace('_', ' ').title()
        
        cuisine_obj, _ = CuisineType.objects.get_or_create(
            api_identifier=raw_type,
            defaults={'name': pretty_name}
        )

        # Create Entry
        UserRestaurantEntry.objects.create(
            user=request.user,
            name=data['name'],
            address=data['address'],
            external_api_id=data['external_api_id'],
            cuisine=cuisine_obj,
            date_picked=timezone.now().date()
        )

        return Response({'status': 'success', 'message': 'Bon Appetit! Saved to history.'})
    
class ReviewCreateUpdateView(APIView):
    """
    Allows a user to add or update a review for a specific history entry.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReviewSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        entry_id = data['entry_id']
        
        # Ensure the history entry belongs to the requesting user
        entry = get_object_or_404(UserRestaurantEntry, id=entry_id, user=request.user)
        
        # Update existing review or create a new one
        review, created = Review.objects.update_or_create(
            entry=entry,
            defaults={
                'rating': str(data['rating']), # Model stores rating as Text
                'comment': data['comment']
            }
        )
        
        return Response({
            'status': 'success', 
            'action': 'created' if created else 'updated',
            'rating': review.rating,
            'comment': review.comment
        }, status=status.HTTP_200_OK)