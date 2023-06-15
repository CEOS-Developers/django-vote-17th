from django.urls import path
from .views import TeamVoteView, CandidateVoteView
app_name = 'vote'

urlpatterns = [
    path('team/', TeamVoteView.as_view(), name='team-vote'),
    path('candidate/', CandidateVoteView.as_view(), name='candidate-vote'),
]