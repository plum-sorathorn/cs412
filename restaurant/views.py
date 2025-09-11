# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/11/2025
# Description:  logic of restaurant webapp. Includes HTTP POST
#               methods and the whole menu. Will receive and process
#               orders and return them as confirmation.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

appetizers = []
main_dishes = []
desserts = []
special_menus = [
    "item1", "item2", "item3",
]

def main(request):
    ''' Main webpage for the restaurant. Simply returns the page. '''

    template_name = "main.html"

    return render(request, template_name)

def order(request):
    ''' Order page. Will display the menu and allow the user to order.
        Also has a daily special function which an item is chosen to be
        displayed randomly. '''
    
    daily_special = random.choice(special_menus)

    payload = {
        'daily_special' : daily_special,
    }
    
    template_name = "order.html"

    return render(request, template_name)

def confirmation(request):
    ''' Confirmation page which will be opened after an order
        is submitted. Will process the submitted order and 
        display the order items. '''
    
    template_name = "confirmation.html"

    if request.POST:
        pass

    return None