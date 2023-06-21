from django.urls import path
from poll import views

urlpatterns = [
    path('', views.PollAPIView.as_view()),
    path('<int:pk>/', views.PollResultAPIView.as_view()),
]
