from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def quotes(request):
    ''' Quotes Page where a random quote and image are generated '''
    template_name = 'quotes.html'
    return render(request, template_name)