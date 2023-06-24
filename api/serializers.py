from rest_framework import serializers
from api.models import *


class DemoVoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['tname']


class CandidateVoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['cname', 'part']


class DemoVoteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['tname', 'count']


class CandidateVoteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['cname', 'part', 'count']