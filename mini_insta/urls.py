# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: url paths for mini_insta webapp

from django.urls import path    
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView

urlpatterns = [
    path('', ProfileListView.as_view(), name="profile_list"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
]