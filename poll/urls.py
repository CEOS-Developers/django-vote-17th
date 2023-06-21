from django.urls import path
from poll import views

urlpatterns = [
    path('', views.PollAPIView.as_view()),
]
