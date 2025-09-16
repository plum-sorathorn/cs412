# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/11/2025
# Description:  logic of restaurant webapp. Includes HTTP POST
#               methods and the whole menu. Will receive and process
#               orders and return them as confirmation.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

appetizers = ["Spring Rolls", "Honey Ribs", "Crying Wings (Spicy Wings)"]
main_dishes = ["Crispy Tamarind Duck", "Thai Omelet with minced pork", "Seafood Stir-fried Curry"]
desserts = ["Coconut Ice Cream", "Thai Pumpkin Custard", "Mango with Sticky Rice"]
special_menus = [
    "Crying Tiger (beef brisket)", "Crying Pork (grilled pork neck)", "Basil Fried Rice",
]

def main(request):
    ''' Main webpage for the restaurant. Simply returns the page. '''

    template_name = "main.html"

    payload = {
        "restaurant_pic" : "restaurant_pic.png",
    }

    return render(request, template_name, payload)

def order(request):
    ''' Order page. Will display the menu and allow the user to order.
        Also has a daily special function which an item is chosen to be
        displayed randomly. '''
    
    daily_special = random.choice(special_menus)

    payload = {
        'appetizers' : appetizers,
        'mains' : main_dishes,
        'desserts' : desserts,
        'daily_special' : daily_special,
    }
    
    template_name = "order.html"

    return render(request, template_name, payload)

def confirmation(request):
    ''' Confirmation page which will be opened after an order
        is submitted. Will process the submitted order and 
        display the order items. '''
    
    template_name = "confirmation.html"

    if request.POST:
        pass

    return None