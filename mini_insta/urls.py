# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: url paths for mini_insta webapp

from django.urls import path    
from .views import ProfileListView

urlpatterns = [
    path('', ProfileListView.as_view(), name="profile_list"),
]
