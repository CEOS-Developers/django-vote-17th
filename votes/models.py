from django.db import models

from accounts.models import User


# Create your models here.

class Team_Vote(models.Model):
    team_list = (
        ('RePick', 'RePick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
        ('Dansupport', 'Dansupport'),
        ('TherapEase', 'TherapEase')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_user')
    team = models.CharField(max_length=16, choices=team_list)

    def __str__(self):
        return f'{self.user.name} : {self.team}'


class Part_Vote(models.Model):
    user_list = (
        ('권가은','권가은'),
        ('김문기','김문기'),
        ('김서연','김서연'),
        ('노수진','노수진'),
        ('배성준','배성준'),
        ('신유진','신유진'),
        ('오예린','이예지'),
        ('장효신','장효신'),
        ('최민주','최민주'),
        ('김지원','김지원'),
        ('김현수','김현수'),
        ('김현우','김현우'),
        ('서찬혁','서찬혁'),
        ('서혜준','서혜준'),
        ('이소정','이소정'),
        ('임탁균','임탁균'),
        ('조예지','조예지'),
        ('최유미','최유미'),
        ('황재령','황재령')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='part_user')
    part = models.CharField(max_length=8, choices=user_list, null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} : {self.part}'
