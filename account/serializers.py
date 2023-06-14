from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SignUpSerializer(serializers.ModelSerializer):

    #추가옵션
    user_id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=50
    )
    part = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    name = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )
    team = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )



    class Meta:
        model = User
        fields = ('user_id','password','email','part','name','team')


    #데이터베이스에 저장
    def save(self, request):
      #print("1")
      user = User.objects.create_user(
          user_id=self.validated_data['user_id'],
          password=self.validated_data['password'],
          email=self.validated_data['email'],
          part=self.validated_data['part'],
          name=self.validated_data['name'],
          team=self.validated_data['team']
      )
      user.save()
      return user



class LoginSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['user_id', 'password']



    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)

        if User.objects.filter(user_id=user_id).exists():
            user = User.objects.get(user_id=user_id)
            part = user.part
            team = user.team

            if not user.check_password(password):
                raise serializers.ValidationError("비밀번호가 틀렸습니다.")
        else:
            raise serializers.ValidationError("존재하지 않는 계정입니다.")

        #user객체로부터 access_token 생성
        token = RefreshToken.for_user(user)
        access_token = str(token.access_token)

        data = {
            'user_id': user_id,
            'user': user,
            'part': part,
            'team': team,
            'access_token': access_token,
        }

        return data
