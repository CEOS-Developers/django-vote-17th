from rest_framework import serializers
from .models import *
from accounts.models import User

class TeamVoteSerializer(serializers.ModelSerializer):
    team_list = (
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
        ('Dansupport', 'Dansupport'),
        ('TherapEase', 'TherapEase')
    )

    team_user = serializers.ReadOnlyField(source='user.name')
    team = serializers.ChoiceField(
        choices=team_list
    )

    class Meta:
        model = Team_Vote
        fields = ['id', 'team_user', 'team']


# class PartVoteSerializer(serializers.ModelSerializer):
#
#     part_user = serializers.ReadOnlyField(source='user.name')
#     part =serializers.CharField(max_length=8)
#     class Meta:
#         model = Team_Vote
#         fields = ['id', 'part_user', 'part']

class PartVoteSerializer(serializers.ModelSerializer):
    user_list = (
        ("권가은", "권가은"),
        ("김문기", "김문기"),
        ("김서연", "김서연"),
        ("노수진", "노수진"),
        ("배성준", "배성준"),
        ("신유진", "신유진"),
        ("오예린", "이예지"),
        ("장효신", "장효신"),
        ("최민주", "최민주"),
        ("김지원", "김지원"),
        ("김현수", "김현수"),
        ("김현우", "김현우"),
        ("서찬혁", "서찬혁"),
        ("서혜준", "서혜준"),
        ("이소정", "이소정"),
        ("임탁균", "임탁균"),
        ("조예지", "조예지"),
        ("최유미", "최유미"),
        ("황재령", "황재령")
    )

    part_user = serializers.ReadOnlyField(source='user.name')
    part = serializers.ChoiceField(
        choices=user_list
    )

    class Meta:
        model=Part_Vote
        fields=['id', 'part_user', 'part']


