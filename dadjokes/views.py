# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: logic for dadjokes API with REST

from django.shortcuts import render
from .models import Joke, Picture
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response

# Create your views here.

class OneJokePictureAPIView(generics.ListAPIView):
    ''' show one Joke and one Picture chosen at random '''
    
    def get_queryset(self):
        return Joke.objects.none()
        
    serializer_class = BothSerializer 

    def list(self, request, *args, **kwargs):
        random_joke = Joke.objects.order_by('?').first()
        random_picture = Picture.objects.order_by('?').first()

        data = {
            'joke': random_joke,
            'picture': random_picture
        }
        
        serializer = self.get_serializer(data)
        
        return Response([serializer.data])

class ListCreateJokeAPIView(generics.ListCreateAPIView):
    '''
    show all Jokes and allow creation of Jokes
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PrimaryJokeAPIView(generics.RetrieveAPIView):
    ''' show one Joke by its primary key '''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class ListCreatePictureAPIView(generics.ListCreateAPIView):
    '''
    allow me to add a picture to the database
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PrimaryPictureAPIView(generics.RetrieveAPIView):
    ''' show one Picture by its primary key '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer