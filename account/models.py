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

    def create_superuser(self, userId=None, name=None, email=None, part=None, team=None, password=None,
                         is_candidate=None, **extra_fields):
        superuser = self.create_user(
            userId=userId,
            name=name,
            email=email,
            part=part,
            team=team,
            password=password,

        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


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
