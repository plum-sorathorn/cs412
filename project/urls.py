# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/24/2025
# Description: url paths for final project

from django.urls import path    
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # GET: /api/cuisines/ -> Lists all cuisine types for filtering
    path('cuisines/', CuisineTypeListView.as_view(), name='cuisine-list'),
    
    # GET: /api/history/ -> Lists the current user's restaurant history
    path('history/', UserHistoryListView.as_view(), name='user-history-list'),

    # AUTHENTICATION ENDPOINTS
    # POST: /project_api/register/ -> Creates new user and returns token
    path('register/', RegisterView.as_view(), name='api-register'),
    
    # POST: /project_api/login/ -> Authenticates user and returns token
    path('login/', LoginView.as_view(), name='api-login'),
]

