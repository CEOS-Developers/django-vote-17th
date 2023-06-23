from django.urls import path
from .views import *

app_name = 'polls'

urlpatterns = [
    path('team-polls/', team_poll_list, name='team_poll_list'),
    path('team-polls/vote/', team_poll_vote, name='team_poll_vote'),
    path('part-polls/', part_poll_list, name='part_poll_list'),
    path('part-polls/vote/', part_poll_vote, name='part_poll_vote'),
]