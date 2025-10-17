# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: logic/backend for mini_insta

from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Photo, Profile, Post
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

# Create your views here.
class ProfileListView(ListView):
    ''' view class to show all mini_insta profiles '''
    
    model = Profile
    template_name = "show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    ''' view class to show individual profiles '''
    model = Profile 
    template_name = "show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    ''' view class to show individual posts '''
    model = Post
    template_name = "show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''A view to create a new post and save it to the database.'''
    
    template_name = "create_post_form.html"
    form_class = CreatePostForm

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        
        context = super().get_context_data()
        
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        form.instance.profile = profile
        form.instance.timestamp = timezone.now()
        post = form.save()

        # # Create a Photo object and associate it with the Post
        # if image_url:
        #     Photo.objects.create(
        #         post=post,
        #         image_url=image_url,
        #         timestamp=timezone.now()
        #     )

        # create photo object and assign all the image files to it
        image_files = self.request.FILES.getlist('image_file')
        while image_files:
            Photo.objects.create(
                post=post,
                image_file=image_files.pop(),
                timestamp=timezone.now()
            )

        return super().form_valid(form)

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
 
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})
    
class UpdateProfileView(UpdateView):
    ''' view class to update individual profiles '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "update_profile_form.html"

class DeletePostView(DeleteView):
    ''' view class to delete posts '''
    model = Post
    template_name = "delete_post_form.html"

    def get_context_data(self, **kwargs):
        ''' Override context to delete specific post '''
        
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        ''' return url page of when post is successfully deleted '''
        post = self.get_object()
        return reverse('profile', kwargs={'pk': post.profile.pk})
    
class UpdatePostView(UpdateView):
    ''' view class to update posts '''
    model = Post
    template_name = "update_post_form.html"
    form_class = UpdatePostForm
    
    def get_context_data(self, **kwargs):
        ''' Override context to delete specific post '''
        
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        ''' return url page of when post is successfully submitted '''
        post = self.get_object()
        return reverse('post', kwargs={'pk': post.pk})
    
class ShowFollowerDetailView(DetailView):
    ''' view class to show this profile's followers '''
    model = Profile
    template_name = "show_followers.html"

    def get_context_data(self, **kwargs):
        ''' Override context to show the profile's followers '''

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profiles'] = profile
        return context
        
class ShowFollowingDetailView(DetailView):
    ''' view class to show profiles that this profile is following '''
    model = Profile
    template_name = "show_following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        ''' Override context to show profile's followings '''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profiles'] = profile
        return context
    
class PostFeedListView(ListView):
    ''' View class to show the post feed for a single profile. '''

    model = Post
    template_name = "show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return the post feed for the profile matching the pk in the URL.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add profile info to the template context.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

class SearchView(ListView):
    ''' View class to search Profiles and Posts based on a text input. '''
    
    template_name = "search_results.html" 
    
    def dispatch(self, request, *args, **kwargs):
        ''' Checks for a 'query'. If absent, shows the search form. 
        If present, proceeds with the ListView process for results. '''
        if 'query' not in self.request.GET:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            return render(request, 'search.html', {'profile': profile})
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        ''' Returns the QuerySet of matching Posts. 
        This is what the ListView mechanism expects. '''
        query = self.request.GET.get('query', '')
        posts = Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        return posts
    
    def get_context_data(self, **kwargs):
        ''' processing logic to filter out searches '''
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        query = self.request.GET.get('query', '')
        
        context['profile'] = profile
        context['query'] = query
        
        context['posts'] = self.object_list
        
        profiles_results = []
        lower_query = query.lower()

        # for loop to compare search text with username, display_name, and         
        for p in Profile.objects.all():

            username_match = lower_query in p.username.lower() if p.username else False
            display_name_match = lower_query in p.display_name.lower() if p.display_name else False
            
            if username_match or display_name_match:
                profiles_results.append(p)

        context['profiles_results'] = profiles_results
        
        return context