# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/6/2025
# Description: file for restaurant webapp urls

from django.urls import path 
from django.conf import settings
from . import views

urlpatterns = [
    path(r'main/', views.main, name="main"),
    path(r'order/', views.order, name="order"),
    path(r'confirmation/', views.confirmation, name="confirmation")
]