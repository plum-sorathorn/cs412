# File: urls.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/6/2025
# Description: file for restaurant webapp urls

from django.urls import path 
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.main_page, name="main_page"),
    path(r'order/', views.order_page, name="order_page")
]