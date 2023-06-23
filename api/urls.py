from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from views import *

urlpatterns = [
    path("auth/signup/", SignUp.as_view()),
    path("auth/signin/", SignIn.as_view()),
    path("auth/signout/", SignOut.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("auth/id/check/", IDCheck.as_view()),
    path("auth/email/check/", EmailCheck.as_view())
]