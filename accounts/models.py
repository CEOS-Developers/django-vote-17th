from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class User(AbstractUser):

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

    name = models.CharField(max_length=8)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    part = models.CharField(max_length=8, choices=part_list, default='백엔드')
    team = models.CharField(max_length=16, choices=team_list, default='바리바리')
    team_vote = models.BooleanField(default=False)
    part_vote = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'name', 'email', 'part', 'team']

    def __str__(self):
        return self.name




