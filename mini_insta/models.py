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
    
    def get_num_posts(self):
        ''' return number of posts associated with this profile '''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts.count()
    
    def get_followers(self):
        ''' return list of followers for this profile '''
        followers = Follow.objects.filter(profile=self)
        followers_list = Profile.objects.filter(pk__in=followers.values('follower_profile')).exclude(username=self.username)
        return followers_list
    
    def get_num_followers(self): 
        ''' return number of follows for this profile '''
        followers = Follow.objects.filter(profile=self)
        followers_list = Profile.objects.filter(pk__in=followers.values('follower_profile')).exclude(username=self.username)
        return  followers_list.count()

    def get_following(self):
        ''' return list of profiles followed by this profile '''
        following = Follow.objects.filter(follower_profile=self)
        following_list = Profile.objects.filter(pk__in=following.values('profile')).exclude(username=self.username)
        return following_list
    
    def get_num_following(self):
        ''' return number of profiles this profile follows '''
        following = Follow.objects.filter(follower_profile=self)
        following_list = Profile.objects.filter(pk__in=following.values('profile')).exclude(username=self.username)
        return following_list.count()
    
    def get_post_feed(self):
        ''' return a post feed, shows posts from profiles followed by this one '''
        following_profiles = self.get_following()
        following_pks = following_profiles
        feed_posts = Post.objects.filter(profile__in=following_pks).order_by('-timestamp')
        return feed_posts
    

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
    
    def get_all_comments(self):
        ''' return all comments associated with this post '''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        ''' return number of likes associated with a post '''
        likes = Like.objects.filter(post=self)
        return likes.count()

class Photo(models.Model):
    ''' model connected to each post, containing each post's photo(s) '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        ''' return string representation of photo '''
        return f'POST INFO: {self.post.profile.username}, {self.post.timestamp}; PHOTO INFO: {self.get_image_url}'

    def get_image_url(self):
        ''' return either the image file or the image url'''
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url

class Follow(models.Model):
    ''' model to connect two nodes (profile to profile) '''
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        ''' return string representation of a follow object '''
        return f'PROFILE: {self.profile.username}; FOLLOWER: {self.follower_profile.username}' 

class Comment(models.Model):
    ''' model for a comment: a profile responding to a post '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        ''' return string representation of a comment object '''
        return f'COMMENT: {self.text} BY: {self.profile.username}'

class Like(models.Model):
    ''' model for a Like: shows approval of a post by a profile '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        ''' return string representation of a like '''
        return f'LIKE BY: {self.profile.username}'