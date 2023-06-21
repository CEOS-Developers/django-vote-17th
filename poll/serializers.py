from rest_framework import serializers
from poll.models import Poll


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
