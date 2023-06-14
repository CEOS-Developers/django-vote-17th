from django.urls import path
from .views import TeamVoteView, CandidateVoteView

urlpatterns = [
    path('teamvote/', TeamVoteView.as_view(), name='team-vote'),
    path('candidatevote/', CandidateVoteView.as_view(), name='candidate-vote'),
]