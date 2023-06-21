from django.urls import path
from .views import *

app_name = 'polls'

urlpatterns = [
    path('team/', teamPollView.as_view()),
    path('part/', partPollView.as_view()),

]