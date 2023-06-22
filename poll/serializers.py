from rest_framework import serializers
from poll.models import Poll, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        poll = Poll(
            name=name
        )
        poll.save()
        return poll


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        depth = 1
        fields = '__all__'

    def create(self, validated_data):
        poll = validated_data.get('poll')
        voter = validated_data.get('voter')
        target_account = validated_data.get('target_account')
        target_team = validated_data.get('target_team')
        vote = Vote(
            poll=poll,
            voter=voter,
            target_account=target_account,
            target_team=target_team,
        )
        vote.save()
        return vote
