# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: logic/backend for mini_insta

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    ''' view class to show all mini_insta profiles '''
    
    model = Profile
    template_name = "show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    ''' view class to show individual profiles '''
    model = Profile 
    template_name = "show_profile.html"
    context_object_name = "profile"