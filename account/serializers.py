from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#User = get_user_model()

class UserSignupSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','name', 'created_at', 'updated_at', 'part', 'team']

    partList = (
        ('backend', 'backend'),
        ('frontend', 'frontend')
    )

    teamList = (
        ('TherapEase', 'TherapEase'),
        ('Dansupport', 'Dansupport'),
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
    )

    username = serializers.CharField(max_length=32) # id
    password = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=8) # 이름
    email = serializers.EmailField()
    part = serializers.ChoiceField(
        choices=partList
    )
    team = serializers.ChoiceField(
        choices=teamList
    )

    def create(self, validated_data):

        if User.objects.filter(username=validated_data['username']).exists() :
            raise serializers.ValidationError('username exists')


        else:
            user = User.objects.create(
                username = validated_data['username'],
                name = validated_data['name'],
                part = validated_data['part'],
                team = validated_data['team'],
                email = validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class LoginSerializer(serializers.Serializer):
 id = serializers.CharField(write_only=True, required=True)
 password = serializers.CharField(write_only=True, required=True)

class RefreshToken(RefreshToken):
    def for_user(cls, user):
        token = super().for_user(user)
        return token

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['id', 'username','password','name', 'created_at', 'updated_at', 'part', 'team','team_vote','part_vote']

    partList = (
        ('backend', 'backend'),
        ('frontend', 'frontend')
    )

    teamList = (
        ('TherapEase', 'TherapEase'),
        ('Dansupport', 'Dansupport'),
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
    )

    username = serializers.CharField(max_length=32)  # id
    password = serializers.CharField(max_length=32, write_only=True)
    name = serializers.CharField(max_length=8)  # 이름
    email = serializers.EmailField()
    part = serializers.ChoiceField(
        choices = partList
    )
    team = serializers.ChoiceField(
        choices = teamList
    )
    teamPoll = serializers.BooleanField(default=False)
    partPoll = serializers.BooleanField(default=False)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
        # if not user.check_password(password):
        #     raise serializers.ValidationError({"Wrong Password"})
        else:
            raise serializers.ValidationError("존재하지 않는 사용자입니다.")

        token = RefreshToken().for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'part': user.part,
            'team': user.team,
            'team_vote': user.team_vote,
            'part_vote': user.part_vote,
        }
        return data