from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, userId, password, email, part, name, team):
        if not userId:
            raise ValueError('userId is required!')
        if not password:
            raise ValueError('password is required!')
        if not email:
            raise ValueError('email is required!')
        if not part:
            raise ValueError('part is required!')
        if not name:
            raise ValueError('name is required!')
        if not team:
            raise ValueError('team is required!')

        user = self.model(
            userId=userId,
            email=email,
            part=part,
            name=name,
            team=team,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, email, password=None):
        user = self.create_user(userId, email, password)

        user.is_superuser = True
        user.is_admin = True
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
    is_admin = models.BooleanField(default=False)

    userId = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    part = models.CharField(max_length=8, choices=partList)
    team = models.CharField(max_length=16, choices=teamList)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['name','password','email','part','team']

    def __str__(self):
        return self.userId

##
