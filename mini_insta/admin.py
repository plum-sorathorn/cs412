# File: admin.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: admin access file for mini_insta

from django.contrib import admin
from .models import Profile, Post, Photo, Follow, Comment, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)