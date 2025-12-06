# File: forms.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 12/05/2025
# Description: forms for backend API (project)

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

# Get the active User model (usually django.contrib.auth.models.User)
User = get_user_model()

# Registration Form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        
    # We can add extra validation or fields here if needed later

# Login Form
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # This custom clean method validates the credentials
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Use Django's built-in authenticate function
            user = authenticate(username=username, password=password)
            
            if user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )
            
            # Store the authenticated user on the form for the view to access
            self.user = user
        
        return self.cleaned_data