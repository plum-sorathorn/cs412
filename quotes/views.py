# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/6/2025
# Description: logic of quotes webapp. Contains quotes, images, and methods to return them.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Quotes as a list of strings
quotes_list = [
    "I'd probably have been wealthier if I had stayed with law, but pretty miserable doing it.",
    "If you behave like a celebrity, then people will treat you like a celebrity, and if you don't, they won't. There's not much to write about me in the tabloids.",
    "I've always felt that the less the public knows about you, the more effective you can be when you go to portray someone else."
]

# Image URLs as a list of strings
images_list = [
    "quotes_cillian_0.jpg",
    "quotes_cillian_1.jpg",
    "quotes_cillian_2.webp"
]

def quotes(request):
    ''' Quotes page where a random quote and image are generated '''
    
    template_name = 'quotes.html'

    random_quote = random.choice(quotes_list)
    random_image = random.choice(images_list)

    context = {
        'generate_random_quote': random_quote,
        'generate_random_image': random_image,
    }

    return render(request, template_name, context)

def show_all(request):
    ''' Show All page where all quotes and images from the list are shown '''

    template_name = 'show_all.html'

    context = {
        'all_quotes': quotes_list,
        'all_images': images_list
    }

    return render(request, template_name, context)