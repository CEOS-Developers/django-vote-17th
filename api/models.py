from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, login_id, email, name, part, team, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not login_id:
            raise ValueError(_('Users must have an ID'))

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            login_id=login_id,
            email=self.normalize_email(email),
            name=name,
            team=team,
            part=part
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login_id, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            login_id=login_id,
            password=password
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseTimeModel, PermissionsMixin):

    PART_CHOICES = [
        ('BE', 'BE'),
        ('FE', 'FE')
    ]

    TEAM_CHOICES = [
        ('DANSUPPRORT', 'Dansupport'),
        ('REPICK', 'Repick'),
        ('THERAPEASE','TherapEase'),
        ('HOOKING', 'Hooking'),
        ('BARIBARI', 'BariBari')
    ]

    login_id = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=10)
    part = models.CharField(max_length=2, choices=PART_CHOICES)
    team = models.CharField(max_length=30, choices=TEAM_CHOICES)


    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login_id


class Team(BaseTimeModel):

    TEAM_CHOCIES = [
        ('DANSUPPORT', 'Dansupport'),
        ('REPICK', 'Repick'),
        ('THERAPEASE', 'TherapEase'),
        ('HOOKING', 'Hooking'),
        ('BARIBARI', 'BariBari')
    ]

    tname = models.CharField(max_length=30, choices=TEAM_CHOCIES, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.tname


class Candidate(BaseTimeModel):

    PART_CHOICES = [
        ('BE', 'BE'),
        ('FE', 'FE')
    ]

    cname = models.CharField(max_length=30, unique=True)
    part = models.CharField(max_length=2, choices=PART_CHOICES)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.cname
