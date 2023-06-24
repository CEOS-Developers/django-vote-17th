from rest_framework import serializers
from account.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    GET polls/vote/part-leader/front-end/
    GET polls/vote/part-leader/back-end/
    GET polls/vote/part-leader/design/
    GET polls/vote/part-leader/project-manager/
    팀 인원 명단을 불러오기 위한 시리얼라이저
    """
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        part = validated_data.get('part')
        team = validated_data.get('team')

        user = User(
            username=username,
            email=email,
            part=part,
            team=team
        )
        user.set_password(password)
        user.save()
        return user



class TeamSerializer(serializers.ModelSerializer):

    """
    GET polls/vote/demo/
    팀 명단을 불러오기 위한 시리얼라이저
    """
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


