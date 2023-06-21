from django.urls import path
from .views import *
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView )
app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('auth/', AuthView.as_view()),
]