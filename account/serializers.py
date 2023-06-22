from rest_framework import serializers
from account.models import *
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
        team_name = validated_data.get('team')
        part_name = validated_data.get('part')
        # 팀, 파트 이름으로 pk 가져오기
        team_pk = Team.objects.get(name__exact=team_name)
        part_pk = Part.objects.get(name__exact=part_name)
        user = User(
            username=username,
            email=email,
            team=team_pk,
            part=part_pk,
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


