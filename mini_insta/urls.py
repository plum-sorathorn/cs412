# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: url paths for mini_insta webapp

from django.urls import path    
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView
from .views import UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowerDetailView
from .views import ShowFollowingDetailView, PostFeedListView, SearchView

urlpatterns = [
    path('', ProfileListView.as_view(), name="profile_list"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/<int:pk>/followers', ShowFollowerDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/search', SearchView.as_view(), name="search"),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name='post_feed'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post")
]