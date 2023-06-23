import logging

from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SignUp(APIView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="회원가입",
        request_body=SignUpRequestSerializer,
        responses={
            201: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        serializer = SignUpRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"code": 201, "messages": "회원가입 성공"}, status=status.HTTP_201_CREATED)

        return Response({"code": 400, "messages": "회원가입 실패"}, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="로그인",
        request_body=SignInRequestSerializer,
        responses={
            200: openapi.Response(
                description="HTTP_200",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="HTTP Code"),
                        'messages': openapi.Schema(type=openapi.TYPE_STRING, description="Messages"),
                        'token': openapi.Schema(type=openapi.TYPE_OBJECT, description="Tokens",
                                                properties={
                                                    'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                   description="Access Token"),
                                                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                    description="Refresh Token")
                                                }
                                                )
                    }
                )
            ),
            400: ResponseSerializer
        }
    )
    def post(self, request):
        login_id = request.data['login_id']
        password = request.data['password']

        user = User.objects.filter(login_id=login_id).first()

        # ID가 존재하지 않는 경우
        if user is None:
            return Response(
                {"code": 400, "message": "회원정보가 일치하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

        # # 비밀번호가 틀린 경우
        if not check_password(password, user.password):
            return Response(
                {"code": 400, "message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면,
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열화
            access_token = str(token.access_token)  # access 토큰 문자열화
            response = Response(
                {
                    "code": 200,
                    "messages": "로그인 성공",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                },
                status=status.HTTP_200_OK
            )

            # response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"code": 400, "message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="로그아웃",
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        if request.user is not None:
            print(request.user)
            response = Response(
                {"code": 200, "message": "로그아웃 성공"}, status=status.HTTP_200_OK
            )
            # response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
        else:
            response = Response(
                {"code": 400, "message": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class IDCheck(APIView):

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="ID 확인",
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        if User.objects.filter(login_id=request.data['login_id']).exists():
            response = Response(
                {"code": 400, "message": "중복된 ID가 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            response = Response(
                {"code": 200, "message": "사용 가능한 ID입니다."}, status=status.HTTP_200_OK
            )

        return response


class EmailCheck(APIView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Email 확인",
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            response = Response(
                {"code": 400, "message": "중복된 email이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        else:
            response = Response(
                {"code": 200, "message": "사용 가능한 email 입니다."}, status=status.HTTP_200_OK
            )

        return response

