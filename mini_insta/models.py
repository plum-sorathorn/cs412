# File: models.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: contains the model of Profile, structure of each user's info

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    ''' structure of each user's data attributes '''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.TextField(blank=True)

    def __str__(self):
        ''' return string representation of profile instance '''
        return f'{self.username}, {self.display_name}'
    
    def get_absolute_url(self):
        ''' return the URL to display instance of this model '''
        return reverse("profile", kwargs={"pk": self.pk})
    
    def get_all_posts(self):
        ''' return QuerySet of posts associated with this profile '''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    

class Post(models.Model):
    ''' model connected to each profile, containing each profile's posts '''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        ''' return string representation of post '''
        return f'USERNAME: {self.profile.username}; TIMESTAMP: {self.timestamp}'
    
    def get_all_photos(self):
        ''' return QuerySet of photos associated with this post '''
        photos = Photo.objects.filter(post=self)
        return photos
    


class Photo(models.Model):
    ''' model connected to each post, containing each post's photo(s) '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        ''' return string representation of photo '''
        return f'POST INFO: {self.post.profile.username}, {self.post.timestamp}; PHOTO INFO: {self.timestamp}'


