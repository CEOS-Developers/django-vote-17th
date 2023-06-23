import jwt
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import AllowAny
from .serializers import UserSignupSerializer,UserLoginSerializer

class SignupView(APIView):
    def post(self, request, format=None):
        user = User.objects.all() #추가
        serializer = UserSignupSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            return Response({'message' : '회원가입 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message' : '회원가입 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            userId=request.data.get("userId"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserLoginSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    'message': '로그인 성공',
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthView(APIView):
 serializer_class = UserLoginSerializer

 def post(self, request, userId=None):
     serializer = self.serializer_class(data=request.data)

     if serializer.is_valid(raise_exception=True):
         userId = serializer.validated_data['userId']
         access = serializer.validated_data['access']
         refresh = serializer.validated_data['refresh']
         #data = serializer.validated_data
         res = Response(
             {
                 "message": "로그인되었습니다.",
                 "id": userId,
                 "access": access,
                 "refresh": refresh
             },
             status=status.HTTP_200_OK,
         )
         return res

     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)