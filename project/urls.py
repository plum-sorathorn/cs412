# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/24/2025
# Description: url paths for final project

from django.urls import path    
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('cuisines/', CuisineTypeListView.as_view(), name='cuisine-list'),
    path('history/', UserHistoryListView.as_view(), name='user-history-list'),
    path('history/delete/<int:pk>/', DeleteHistoryEntryView.as_view(), name='delete-history'),
    
    # review
    path('review/', ReviewCreateUpdateView.as_view(), name='add-review'),

    # AUTHENTICATION ENDPOINTS
    path('register/', RegisterView.as_view(), name='api-register'),
    
    path('login/', LoginView.as_view(), name='api-login'),

    # filtering and logging
    path('filter-restaurants/', RestaurantFilterView.as_view(), name='filter-restaurants'),
    path('suggest-cuisines/', CuisineSuggestionView.as_view(), name='suggest-cuisines'),
    path('log-visit/', LogVisitView.as_view(), name='log-visit'),

]

