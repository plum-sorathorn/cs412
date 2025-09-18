# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/11/2025
# Description:  logic of restaurant webapp. Includes HTTP POST
#               methods and the whole menu. Will receive and process
#               orders and return them as confirmation.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

appetizers = ["Spring Rolls", "Honey Ribs", "Crying Wings (spicy wings)"]
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

        # Get all selected items using getlist()
        selected_appetizers = request.POST.getlist("appetizer")
        selected_mains = request.POST.getlist("main")
        selected_desserts = request.POST.getlist("dessert")
        selected_special = request.POST.getlist("special")

        # Combine all selected items into one list
        ordered_items = []
        ordered_items.extend(selected_appetizers)
        ordered_items.extend(selected_mains)
        ordered_items.extend(selected_desserts)
        ordered_items.extend(selected_special)

        # Handle "Crying Wings" spice level if it was selected
        spice_level = None
        if "Crying Wings (Spicy Wings)" in ordered_items:
            spice_level = request.POST.get("spice", "Not specified")

        # special instructions
        special_instructions = request.POST.get("special_instructions", "N/A")

        # Get customer information from the form
        customer_name = request.POST.get("name", "N/A")
        customer_phone = request.POST.get("phone", "N/A")
        customer_email = request.POST.get("email", "N/A")

        payload = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'spice_level': spice_level,
        }
        
        return render(request, template_name, payload)

    return render(request, template_name)