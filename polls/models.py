from django.db import models
from account.models import *

class teamPoll(models.Model):
    teamChoices = (
        ('TherapEase', 'TherapEase'),
        ('Dansupport', 'Dansupport'),
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
    )
    team = models.CharField(max_length=10, choices=teamChoices)
    description = models.CharField(max_length=200, default=None)
    name = models.CharField(max_length=10) # 투표자 이름
    voteNum = models.IntegerField(default=0)

    def __str__(self):
        return self.team


class partPoll(models.Model):
    partChoices = {
        ('back', 'Back-end'),
        ('front', 'Front-end'),
    }

    candidatesChoices = {
        ('황재령', '황재령'),
        ('김지원', '김지원'),
        ('김현수', '김현수'),
        ('김현우', '김현우'),
        ('서찬혁', '서찬혁'),
        ('서혜준', '서혜준'),
        ('이소정', '이소정'),
        ('임탁균', '임탁균'),
        ('조예지', '조예지'),
        ('최유미', '최유미'),
        ('권가은', '권가은'),
        ('김문기', '김문기'),
        ('김서연', '김서연'),
        ('노수진', '노수진'),
        ('배성준', '배성준'),
        ('신유진', '신유진'),
        ('오예린', '이예지'),
        ('장효신', '장효신'),
        ('최민주', '최민주'),
    }
    part = models.CharField(max_length=10, choices=partChoices)
    userName = models.CharField(max_length=10)
    voteNum = models.IntegerField(default=0)
    candidate = models.CharField(max_length=10, choices=candidatesChoices)
    def __str__(self):
        return self.candidate