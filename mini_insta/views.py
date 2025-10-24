# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: logic/backend for mini_insta

from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Photo, Profile, Post, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm

# Create your views here.
class ProfileListView(ListView):
    ''' view class to show all mini_insta profiles '''
    
    model = Profile
    template_name = "show_all_profiles.html"
    context_object_name = "profiles"

class  CreateProfileView(CreateView):
    ''' view class to register and create a profile '''
    model = Profile
    template_name = "create_profile_form.html"
    form_class = CreateProfileForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        form = UserCreationForm()
        data['userdata'] = form
        return data

    def form_valid(self, form):
        ''' handles the creation of the user and logging them in before saving the profile '''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
        return super().form_valid(form)
    

class ProfileDetailView(DetailView):
    ''' view class to show individual profiles '''
    model = Profile 
    template_name = "show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_to_view = self.object

        # Add flags for the logged-in user if authenticated
        if self.request.user.is_authenticated:
            is_following = profile_to_view.is_followed_by_user(self.request.user)
            context['is_following'] = is_following
            
        return context

class PostDetailView(DetailView):
    ''' view class to show individual posts '''
    model = Post
    template_name = "show_post.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Add flags for the logged-in user if authenticated
        if self.request.user.is_authenticated:
            is_liked = post.is_liked_by_user(self.request.user)
            context['is_liked'] = is_liked
            
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to create a new post and save it to the database.'''
    
    template_name = "create_post_form.html"
    form_class = CreatePostForm

    # authentication
    login_url = "/login/"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('mini_insta/login') 

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        
        context = super().get_context_data()
        
        profile = Profile.objects.get(user=self.request.user)
        
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
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' view class to update individual profiles '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "update_profile_form.html"
    
    # authentication
    login_url = "/login/"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_object(self):
        ''' get profile object for this user '''
        return get_object_or_404(Profile, user=self.request.user)

class DeletePostView(LoginRequiredMixin, DeleteView):
    ''' view class to delete posts '''
    model = Post
    template_name = "delete_post_form.html"

    # authentication
    login_url = "/login/"

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
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    ''' view class to update posts '''
    model = Post
    template_name = "update_post_form.html"
    form_class = UpdatePostForm

    # authentication
    login_url = "/login/"
    
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
    
class PostFeedListView(LoginRequiredMixin, ListView):
    ''' View class to show the post feed for a single profile. '''

    model = Post
    template_name = "show_feed.html"
    context_object_name = "posts"

    # authentication
    login_url = "/login/"

    def get_queryset(self):
        '''Return the post feed for the profile matching the pk in the URL.'''
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add profile info and is_liked status to the template context.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        
        # Iterate over all posts to check the like status for the logged-in user
        if self.request.user.is_authenticated:
            for post in context['posts']:
                post.is_liked = post.is_liked_by_user(self.request.user)
        
        return context

class SearchView(LoginRequiredMixin, ListView):
    ''' View class to search Profiles and Posts based on a text input. '''
    
    template_name = "search_results.html"
    
    # authentication
    login_url = "/login/"
    
    def dispatch(self, request, *args, **kwargs):
        ''' Checks for a 'query'. If absent, shows the search form. 
        If present, proceeds with the ListView process for results. '''
        if 'query' not in self.request.GET:
            profile = Profile.objects.get(user=self.request.user)
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

        profile = Profile.objects.get(user=self.request.user)
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
    
class LogoutConfirmationView(TemplateView):
    template_name = "logged_out.html"


# Likes and Follow views
class FollowProfileView(LoginRequiredMixin, TemplateView):
    ''' View to follow a profile. '''
    
    template_name = "placeholder.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        ''' Performs the follow action and redirects. '''
        profile_to_follow = get_object_or_404(Profile, pk=kwargs['pk'])
        
        follower_profile = get_object_or_404(Profile, user=request.user)

        # Check: Do not allow a Profile to follow itself
        if follower_profile != profile_to_follow:
            # Check if a Follow object already exists
            existing_follow = Follow.objects.filter(
                profile=profile_to_follow,
                follower_profile=follower_profile
            ).exists()

            if not existing_follow:
                # Create the Follow object
                Follow.objects.create(
                    profile=profile_to_follow,
                    follower_profile=follower_profile,
                    timestamp=timezone.now()
                )

        return redirect('profile', pk=profile_to_follow.pk)


class DeleteFollowView(LoginRequiredMixin, TemplateView):
    ''' View to unfollow a profile. '''
    
    template_name = "placeholder.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        ''' Performs the unfollow action and redirects. '''
        
        profile_to_unfollow = get_object_or_404(Profile, pk=kwargs['pk'])
        follower_profile = get_object_or_404(Profile, user=request.user)

        # Find and delete the Follow object
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower_profile
        ).delete()
        
        # Redirect back to the profile page of the person who was unfollowed
        return redirect('profile', pk=profile_to_unfollow.pk)


class LikePostView(LoginRequiredMixin, TemplateView):
    ''' View to like a post. '''
    
    template_name = "placeholder.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        ''' Performs the like action and redirects. '''
        post = get_object_or_404(Post, pk=kwargs['pk'])
        liking_profile = get_object_or_404(Profile, user=request.user)

        # Check: Do not allow a Profile to like it's own Post
        if liking_profile != post.profile:
            # Check if a Like object already exists
            existing_like = Like.objects.filter(
                post=post,
                profile=liking_profile
            ).exists()
            
            if not existing_like:
                # Create the Like object
                Like.objects.create(
                    post=post,
                    profile=liking_profile,
                    timestamp=timezone.now()
                )
        
        # Redirect back to the post's detail page
        return redirect('post', pk=post.pk)


class DeleteLikeView(LoginRequiredMixin, TemplateView):
    ''' View to unlike a post. '''
    
    template_name = "placeholder.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        ''' Performs the unlike action and redirects. '''
        # Post being unliked
        post = get_object_or_404(Post, pk=kwargs['pk'])

        liking_profile = get_object_or_404(Profile, user=request.user)

        # Find and delete the Like object
        Like.objects.filter(
            post=post,
            profile=liking_profile
        ).delete()
        
        # Redirect back to the post's detail page
        return redirect('post', pk=post.pk)