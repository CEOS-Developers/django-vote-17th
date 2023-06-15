from rest_framework import serializers
from account.models import *
from vote.models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team', 'vote_cnt']


class TeamVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamVote
        fields = [ 'team','user_name'] # user_name 추가

    # def save(self,request):
    #     team = Team.objects.create_user(
    #         user_id=self.validated_data['user_id'],
    #         team=self.validated_data['team']
    #     )
    #     team.save()
    #     return team


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name', 'part', 'vote_cnt']


class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVote
        fields = ['candidate', 'user_name']  # user_name 추가