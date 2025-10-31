# File: views.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 10/29/2025
# Description: logic/backend for voter_analytics

from datetime import date
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.graph_objects as go
import plotly.offline as opy

parties = [
    'U', 'D', 'R', 'J', 'A', 'CC', 'X', 'L', 'Q', 'S', 'FF', 'G',
    'HH', 'T', 'AA', 'GG', 'Z', 'O', 'P', 'E', 'V', 'H', 'Y', 'W',
    'EE', 'K'
]
date_of_births = [str(year) for year in range(1920, 2005)]
voter_scores = [str(i) for i in range(6)]
elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

class VoterListView(ListView):
    ''' load page of all voters '''
    model = Voter
    template_name = "show_all_voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        ''' return filtered list of voters '''
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
        ''' provide selection for filters '''
        context = super().get_context_data(**kwargs)

        context['parties'] = parties
        context['date_of_births'] = date_of_births
        context['voter_scores'] = voter_scores
        context['elections'] = elections

        return context
    
class VoterDetailView(DetailView):
    ''' return individual voter data '''
    model = Voter
    template_name = 'show_voter.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView):
    model = Voter
    template_name = 'graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        ''' return filtered list of voters '''
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

    def get_context_data(self, **kwargs) :
        '''
        Provide graphs for this template
        '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
 
        # Histogram (Bar Chart): Distribution of Voters by Year of Birth
        
        # aggregate year of births
        birth_year_counts = {}
        for voter in voters:
            if voter.date_of_birth:
                year = voter.date_of_birth.year
                birth_year_counts[year] = birth_year_counts.get(year, 0) + 1
        
        # sort by year
        x_birth = sorted([year for year in birth_year_counts.keys()])
        y_birth = [birth_year_counts[year] for year in x_birth]

        # generate the Bar chart
        fig = go.Bar(x=x_birth, y=y_birth)
        title_text = "Distribution of Voters by Year of Birth"
        
        # obtain the graph as an HTML div
        graph_div_birth_year = opy.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         "layout": {"xaxis": {"title": "Year of Birth"},
                                                    "yaxis": {"title": "Number of Voters"}}
                                        }, 
                                        auto_open=False, 
                                        output_type="div")
        # send div as template context variable
        context['graph_div_birth_year'] = graph_div_birth_year

        # Pie Chart: Distribution of Voters by Party Affiliation
        
        # aggregate party affiliations
        party_counts = {}
        for voter in voters:
            if voter.party_affiliation:
                party = voter.party_affiliation
                party_counts[party] = party_counts.get(party, 0) + 1
        
        # Prepare labels and values for the chart
        x_party = list(party_counts.keys())
        y_party = list(party_counts.values())

        # generate the Pie chart
        fig = go.Pie(labels=x_party, values=y_party)
        title_text = "Voter Party Affiliation Distribution"
        
        # obtain the graph as an HTML div
        graph_div_party = opy.plot({"data": [fig], 
                                    "layout_title_text": title_text,
                                   }, 
                                   auto_open=False, 
                                   output_type="div")
        # send div as template context variable
        context['graph_div_party'] = graph_div_party

        # Histogram (Bar Chart): Distribution of Voters by Election Participation
        
        election_data = []
        # Iterate through the election fields and count voters who participated
        for election in elections:
            count = voters.filter(**{f"{election}": True}).count()
            election_data.append(count)
        
        # generate the Bar chart
        x_elections = elections 
        y_elections = election_data
        
        fig = go.Bar(x=x_elections, y=y_elections)
        title_text = "Voter Participation in Each Election"
        
        # obtain the graph as an HTML div
        graph_div_election_participation = opy.plot({"data": [fig], "layout_title_text": 
                                                        title_text,"layout": {"xaxis": {"title": "Election"},
                                                                              "yaxis": {"title": "Number of Voters"}}
                                                    }, 
                                                    auto_open=False, 
                                                    output_type="div")
        context['graph_div_election_participation'] = graph_div_election_participation

        # add filtering payload to context

        context['parties'] = parties
        context['date_of_births'] = date_of_births
        context['voter_scores'] = voter_scores
        context['elections'] = elections

        return context

        return context