from rest_framework import serializers
from account.models import *
from vote.models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'voteCount']


class TeamVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamVote
        fields = ['id', 'userPk', 'teamPk']


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'part', 'voteCount']


class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVote
        fields = ['id', 'userPk', 'candidatePk']