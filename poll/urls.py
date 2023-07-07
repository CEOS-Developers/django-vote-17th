from django.urls import path
from poll import views

urlpatterns = [
    path('', views.PollAPIView.as_view()),
    path('vote/demo/', views.DemoVoteAPIView.as_view()),
    path('demo/', views.DemoResultAPIView.as_view()),
    # TODO : PartLeaderAPIView 관련 path 구현
    path('vote/part-leader/<str:part>/', views.PartLeaderVoteAPIView.as_view()),
    path('part-leader/<str:part>/', views.PartLeaderResultAPIView.as_view()),
    path('vote-history/<str:userid>/', views.CheckVoteAPIView.as_view()),
]
