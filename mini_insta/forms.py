# File: forms.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: contains the class for the form to create posts

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    ''' form to add a post to a profile '''
    class Meta:
        ''' link form to model in database '''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    ''' form to update a profile '''
    class Meta:
        ''' link form to model in database '''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    ''' form to update a post '''
    class Meta:
        ''' link form to model in database '''
        model = Post
        fields = ['caption']