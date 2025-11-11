# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: url paths for dadjokes api

from django.urls import path   
from .views import ListCreateJokeAPIView, ListCreatePictureAPIView

urlpatterns = [
    path('api/jokes', ListCreateJokeAPIView.as_view(), name="create_list_joke_api"),
    path('api/pictures', ListCreatePictureAPIView.as_view(), name="create_list_picture_api"),
]