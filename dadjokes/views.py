# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: logic for dadjokes API with REST

from django.shortcuts import render
from .models import Joke, Picture
from rest_framework import generics
from .serializers import *

# Create your views here.

class ListCreateJokeAPIView(generics.ListCreateAPIView):
    '''
    allow me to add a joke to the database
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class ListCreatePictureAPIView(generics.ListCreateAPIView):
    '''
    allow me to add a picture to the database
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer