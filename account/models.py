from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager  # 임포트
from datetime import datetime

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #생성 시간
    updated_at = models.DateTimeField(auto_now=True) #수정 시간

    class Meta:
        abstract = True #상속 허용

    def delete(self, using=None, keep_parents=False): #soft delete
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()


class UserManager(BaseUserManager):
    # 필수로 필요한 데이터를 선언
    def create_user(self, user_id, password, email, part, name, team):
        if not user_id:
            raise ValueError('아이디 입력은 필수입니다.')
        if not password:
            raise ValueError('비밀번호 입력은 필수입니다.')
        if not email:
            raise ValueError('이메일 입력은 필수입니다.')
        if not part:
            raise ValueError('파트 선택은 필수입니다.')
        if not name:
            raise ValueError('이름 입력은 필수입니다.')
        if not team:
            raise ValueError('팀 선택은 필수입니다.')

        user = self.model(
            user_id=user_id,
            email=email,
            part=part,
            name=name,
            team=team,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, user_id, email, password=None):
        user = self.create_user(
            email=email,
            user_id=user_id,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # DB에 저장할 데이터
    name = models.CharField("이름", max_length=20, unique=True)
    user_id = models.CharField("ID", max_length=20, unique=True)
    email = models.EmailField("이메일", max_length=50, unique=True)
    part = models.CharField("파트", max_length=20)
    team = models.CharField("팀", max_length=20)
    is_teamvote = models.BooleanField("팀투표 여부", default=False)
    is_partvote = models.BooleanField("파트장투표 여부", default=False)

    # 활성화 여부 (기본값은 True) => 필수 설정
    is_active = models.BooleanField(default=True)

    # 관리자 권한 여부 (기본값은 False) => 필수 설정
    is_admin = models.BooleanField(default=False)


    REQUIRED_FIELDS = ['password','part','name','team']
    USERNAME_FIELD = 'user_id'

    # custom user 생성 시 필요
    objects = UserManager()


    def __str__(self):
        return f"{self.user_id} / {self.email}님의 계정입니다"


