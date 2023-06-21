from django.urls import path
from poll import views

urlpatterns = [
    path('', views.PollAPIView.as_view()),
    path('<str:poll_type>/', views.PollResultAPIView.as_view()),
]
