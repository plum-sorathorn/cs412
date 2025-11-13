# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: url paths for dadjokes api

from django.urls import path   
from .views import *

urlpatterns = [
    path('api/', OneJokePictureAPIView.as_view(), name="joke_picture_api"),
    path('api/random', OneJokePictureAPIView.as_view(), name="random_joke_picture_api"),
    path('api/jokes', ListCreateJokeAPIView.as_view(), name="create_list_joke_api"),
    path('api/joke/<pk>', PrimaryJokeAPIView.as_view(), name="primary_joke_api"),
    path('api/pictures', ListCreatePictureAPIView.as_view(), name="create_list_picture_api"),
    path('api/picture/<pk>', PrimaryPictureAPIView.as_view(), name="primary_picture_api"),
]