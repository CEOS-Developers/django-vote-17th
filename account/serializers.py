from rest_framework import serializers
from account.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        team = Team(
            name=name
        )
        team.save()
        return team
