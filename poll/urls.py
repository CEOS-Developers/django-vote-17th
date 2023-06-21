from django.urls import path
from poll import views

urlpatterns = [
    path('', views.PollAPIView.as_view()),
    path('vote/demo/', views.DemoVoteAPIView.as_view()),
    path('demo/', views.DemoResultAPIView.as_view()),
    # TODO : PartLeaderAPIView 관련 path 구현
]
