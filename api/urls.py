from django.urls import path, include
from . import views

urlpatterns = [
    path('votes/candidates/', views.CandidateVoteAPIView.as_view()),
    path('votes/candidates/fe/', views.FEVoteResultAPIView.as_view()),
    path('votes/candidates/be/', views.BEVoteResultAPIView.as_view()),
    path('votes/teams/', views.DemoVoteAPIView.as_view()),
    path('votes/teams/result/', views.DemoVoteResultAPIView.as_view())
]