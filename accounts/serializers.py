from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=['id', 'username','password','name', 'created_at', 'updated_at', 'part', 'team']

    part_list = (
        ('프론트엔드', '프론트엔드'),
        ('백엔드', '백엔드')
    )

    team_list = (
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
        ('Dansupport', 'Dansupport'),
        ('TherapEase', 'TherapEase')
    )

    username = serializers.CharField(max_length=32) # 아이디
    password = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=8) # 이름
    part = serializers.ChoiceField(
        choices=part_list
    )
    team = serializers.ChoiceField(
        choices=team_list
    )

    def create(self, validated_data):

        if User.objects.filter(username=validated_data['username']).exists() or User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('username 존재 or email 존재')


        else:
            user = User.objects.create(
                username=validated_data['username'],
                name=validated_data['name'],
                email=validated_data['email'],
                part=validated_data['part'],
                team=validated_data['team']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class UserLoginSerializer(serializers.Serializer):

    class Meta:
        model=User
        fields=['id', 'username','password','name', 'created_at', 'updated_at', 'part', 'team','team_vote','part_vote']

    part_list = (
        ('프론트엔드', '프론트엔드'),
        ('백엔드', '백엔드')
    )

    team_list = (
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
        ('Dansupport', 'Dansupport'),
        ('TherapEase', 'TherapEase')
    )

    username = serializers.CharField(max_length=32)  # 아이디
    password = serializers.CharField(max_length=32, write_only=True)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=8)  # 이름
    part = serializers.ChoiceField(
        choices=part_list
    )
    team = serializers.ChoiceField(
        choices=team_list
    )
    team_vote =serializers.BooleanField(default=False)
    part_vote = serializers.BooleanField(default=False)

    def validate(self, data):
        username=data.get("username", None)
        password=data.get("password", None)

        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username)

            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호')
        else:
            raise serializers.ValidationError("존재하지 않는 유저")


        data = {
            'id': user.id,
            'username':user.username,
            'name' : user.name,
            'part' : user.part,
            'team' : user.team,
            'team_vote' : user.team_vote,
            'part_vote': user.part_vote,
        }
        return data
