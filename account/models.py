from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, nickname, **extra_fields):
        if not username:
            raise ValueError('username Required!')

        user = self.model(
            username=username,
            nickname=nickname,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, nickname=None):
        user = self.create_user(username, password, nickname)

        user.is_superuser = True
        user.is_staff = True
        user.level = 0

        user.save(using=self._db)
        return user



class User(AbstractUser):
    objects = UserManager()
    partList = (
        ('backend','backend'),
        ('frontend', 'frontend'),
    )

    teamList = (
        ('TherapEase', 'TherapEase'),
        ('Dansupport', 'Dansupport'),
        ('RePick', 'Repick'),
        ('바리바리', '바리바리'),
        ('Hooking', 'Hooking'),
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    name = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    part = models.CharField(max_length=8, choices=partList)
    team = models.CharField(max_length=16, choices=teamList)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','password','email','part','team']

    def __str__(self):
        return self.name

##
