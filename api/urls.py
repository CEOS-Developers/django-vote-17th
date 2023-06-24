from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *

urlpatterns = [
    path("auth/signup/", SignUp.as_view()),
    path("auth/signin/", SignIn.as_view()),
    path("auth/signout/", SignOut.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("auth/id/check/", IDCheck.as_view()),
    path("auth/email/check/", EmailCheck.as_view()),
    path('votes/candidates/', CandidateVoteAPIView.as_view()),
    path('votes/candidates/fe/', FEVoteResultAPIView.as_view()),
    path('votes/candidates/be/', BEVoteResultAPIView.as_view()),
    path('votes/teams/', DemoVoteAPIView.as_view()),
    path('votes/teams/result/', DemoVoteResultAPIView.as_view()),
    path('votes/candidates/authority', CandiVoteAuthority.as_view()),
    path('votes/teams/authority', CandiVoteAuthority.as_view())
]

