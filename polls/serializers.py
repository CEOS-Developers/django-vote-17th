from rest_framework import serializers
from account.models import *
from polls.models import *

class TeamPollSerializer(serializers.ModelSerializer):

    class Meta:
        model = teamPoll
        fields = ['userId', 'team', 'voteCnt']


class PartPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = partPoll
        fields = ['userId', 'candidate', 'voteCnt']