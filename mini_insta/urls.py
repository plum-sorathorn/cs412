# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: url paths for mini_insta webapp

from django.urls import path    
from django.contrib.auth import views as auth_views
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView
from .views import UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowerDetailView
from .views import ShowFollowingDetailView, PostFeedListView, SearchView, LogoutConfirmationView
from .views import CreateProfileView, FollowProfileView, DeleteFollowView, LikePostView, DeleteLikeView

urlpatterns = [
    # profiles
    path('', ProfileListView.as_view(), name="profile_list"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/followers', ShowFollowerDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/search', SearchView.as_view(), name="search"),
    path('profile/feed', PostFeedListView.as_view(), name='post_feed'),

    # posting
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    
    # login and out
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logged_out/', LogoutConfirmationView.as_view(), name='logout_confirmation'),

    #  following
    path('profile/<int:pk>/follow/', FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/delete_follow/', DeleteFollowView.as_view(), name='delete_follow'),
    
    # liking
    path('post/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/delete_like/', DeleteLikeView.as_view(), name='delete_like'),

]