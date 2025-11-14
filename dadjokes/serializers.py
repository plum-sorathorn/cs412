# File: serializer.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 11/11/2025
# Description: 
#   file to convert our django data models
#   for transmission as text over HTTP

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the Joke model.
    Specifies which fields are exposed in the API
    '''

    class Meta:
        model = Joke 
        fields = ['text','name','timestamp']

    def create(self, validated_data):
        joke = Joke.object.create(**validated_data)
        joke.save()
        return joke 

class PictureSerializer(serializers.ModelSerializer):
    ''' 
    A serializer class for the Picture model
    specifies which fields are exposed in the API
    '''

    class Meta:
        model = Picture
        fields = ['image_url','name','timestamp']

    def create(self, validated_data):
        ''' handle object creation '''
        picture = Picture.object.create(**validated_data)
        picture.save()
        return picture

class BothSerializer(serializers.Serializer):
    """
    A serializer to combine the random Joke and random Picture data.
    """
    joke = JokeSerializer()
    picture = PictureSerializer()