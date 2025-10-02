from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    ''' form to add a post to a profile '''
    class Meta:
        ''' link form to model in database '''
        model = Post
        fields = ['caption']
