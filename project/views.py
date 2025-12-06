# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/24/2025
# Description: views for backend API (project)

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

class RegisterView(APIView):
    """ Handles user registration and returns a token upon success. """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
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
    
    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use Django form to authenticate credentials
        form = UserLoginForm(data=serializer.validated_data)

        if form.is_valid():
            user = form.user # User is attached to the form during clean()
            
            # Use Django's login function to set a session (optional for pure API)
            login(request, user)
            
            # Retrieve the token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response(TokenSerializer({'token': token.key}).data)
        
        # If authentication fails
        return Response(form.errors, status=status.HTTP_401_UNAUTHORIZED)