# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 10/29/2025
# Description: logic/backend for voter_analytics

from datetime import date
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

parties = [
    'U', 'D', 'R', 'J', 'A', 'CC', 'X', 'L', 'Q', 'S', 'FF', 'G',
    'HH', 'T', 'AA', 'GG', 'Z', 'O', 'P', 'E', 'V', 'H', 'Y', 'W',
    'EE', 'K'
]
date_of_births = [str(year) for year in range(1920, 2005)]
voter_scores = [str(i) for i in range(6)]
elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

class VoterListView(ListView):
    model = Voter
    template_name = "show_all_voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        voters = super().get_queryset()

        # Filter by party
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = Voter.objects.filter(party_affiliation=party)

        # Filter by min and max year of birth
        if 'min_dob_year' in self.request.GET and 'max_dob_year' in self.request.GET:
            min_year = self.request.GET['min_dob_year']
            max_year = self.request.GET['max_dob_year']
            if min_year and max_year:
                voters = voters.filter(date_of_birth__year__range=[min_year, max_year])

        # Filter by voter score
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        # Filter by previous election participation
        for election in self.request.GET:
            if election in elections and self.request.GET.get(election) == 'on':
                voters = voters.filter(**{f"{election}": True})

        return voters
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['parties'] = parties
        context['date_of_births'] = date_of_births
        context['voter_scores'] = voter_scores
        context['elections'] = elections

        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'show_voter.html'
    context_object_name = 'voter'