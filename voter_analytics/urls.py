# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 10/29/2025
# Description: url paths for voter_analytics webapp

from django.urls import path   
from .views import VoterListView, VoterDetailView, VoterGraphsView

urlpatterns = [
    path('', VoterListView.as_view(), name="voter_list"),
    path('voters/<int:pk>', VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]