import jwt
from django.shortcuts import render
import logging
from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.serializers import *
from django_vote_17th import settings
from django_vote_17th.settings import SECRET_KEY

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
                        ),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description="User",
                                                properties={
                                                    'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                   description="User Name"),
                                                    'part': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                    description="User Part"),
                                                    'team': openapi.Schema(type=openapi.TYPE_STRING,
                                                                           description="User Team"),
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
                    },
                    "user": {
                        "name": user.name,
                        "part": user.part,
                        "team": user.team
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
    def get(self, request):
        if request.user is not None:
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
        request_body=IdCheckSerializer,
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
        request_body=EmailCheckSerializer,
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


class TokenRefreshView(APIView):

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="token refresh",
        responses={
            201: openapi.Response(
                description="HTTP_201",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="HTTP Code"),
                        'messages': openapi.Schema(type=openapi.TYPE_STRING, description="Messages"),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description="User",
                                               properties={
                                                   'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                          description="User Name"),
                                                   'part': openapi.Schema(type=openapi.TYPE_STRING,
                                                                          description="User Part"),
                                                   'team': openapi.Schema(type=openapi.TYPE_STRING,
                                                                          description="User Team"),
                                               }
                                               )
                    }
                )
            ),
            400: ResponseSerializer
        }
    )
    def post(self, request):
        refresh = request.COOKIES['refresh_token']

        if refresh is None:
            return Response(
                {"code": 400, "message": "refresh token이 존재하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = jwt.decode(
                refresh, SECRET_KEY, algorithms=['HS256']
            )
        except:
            return Response(
                {"code": 400, "message": "refresh token 만료"}, status=status.HTTP_400_BAD_REQUEST
            )

        print(payload)
        user = User.objects.get(id=payload['user_id'])

        if user is None:
            return Response(
                {"code": 400, "message": "refresh token 만료"}, status=status.HTTP_400_BAD_REQUEST
            )

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)

        return Response(
                {
                    "code": 200,
                    "messages": "access token 재발급",
                    "access_token": access_token,
                    "user": {
                        "name": user.name,
                        "part": user.part,
                        "team": user.team
                    }
                },
                status=status.HTTP_200_OK
            )


class DemoVoteAuthority(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="Demo 투표 권한 확인",
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            401: ResponseSerializer
        }
    )
    def get(self, request):
        if request.user.isDemoVoted is False:
            response = Response(
                {"code": 200, "message": "투표 권한 존재"}, status=status.HTTP_200_OK
            )
        elif request.user.isDemoVoted is True:
            response = Response(
                {"code": 400, "message": "투표 권한 없음"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            response = Response(
                {"code": 401, "message": "로직 에러"}, status=status.HTTP_401_BAD_REQUEST
            )
        return response


class CandiVoteAuthority(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="Candidate 투표 권한 확인",
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            401: ResponseSerializer
        }
    )
    def get(self, request):
        if request.user.isCandiVoted is False:
            response = Response(
                {"code": 200, "message": "투표 권한 존재"}, status=status.HTTP_200_OK
            )
        elif request.user.isCandiVoted is True:
            response = Response(
                {"code": 400, "message": "투표 권한 없음"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            response = Response(
                {"code": 401, "message": "로직 에러"}, status=status.HTTP_401_BAD_REQUEST
            )
        return response


class CandidateVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="파트장 투표",
        request_body=CandidateVoteRequestSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        part = request.data['part']
        if request.user.part == part:
            cname = request.data['cname']
            candidate = Candidate.objects.get(cname=cname)
            candidate.count = candidate.count + 1
            candidate.save()
            response = Response(
                {"code": 200, "message": "파트장 투표 참여 성공."}, status=status.HTTP_200_OK
            )
            # User의 isCandiVote 값 변경해주기
            request.user.isCandiVoted = True
            request.user.save()
        else:
            response = Response(
                {"code": 400, "message": "소속된 파트가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class FEVoteResultAPIView(APIView):

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="FE 파트장 결과",
        responses={
            200: CandidateVoteResponseSerializer
        }
    )
    def get(self, request):
        candidatelist = Candidate.objects.filter(part='fe').order_by('-count')
        serializer = CandidateVoteResponseSerializer(candidatelist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BEVoteResultAPIView(APIView):

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="BE 파트장 결과",
        responses={
            200: CandidateVoteResponseSerializer
        }
    )
    def get(self, request):
        candidatelist = Candidate.objects.filter(part='be').order_by('-count')
        serializer = CandidateVoteResponseSerializer(candidatelist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DemoVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="데모데이 투표",
        request_body=DemoVoteRequestSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer
        }
    )
    def post(self, request):
        tname = request.data['tname']
        print(tname)
        print(request.user.team)
        if request.user.team == tname:
            response = Response(
                {"code": 400, "message": "소속된 팀에는 투표하실 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            team = Team.objects.get(tname=tname)
            team.count = team.count + 1
            team.save()
            response = Response(
                {"code": 200, "message": "데모데이 투표 참여 성공."}, status=status.HTTP_200_OK
            )
            # User의 isCandiVote 값 변경해주기
            request.user.isDemoVoted = True
            request.user.save()
        return response


class DemoVoteResultAPIView(APIView):
    @swagger_auto_schema(
        tags=["votes"],
        operation_summary="데모데이 결과",
        responses={
            200: DemoVoteResponseSerializer
        }
    )
    def get(self, request):
        teamlist = Team.objects.all().order_by('-count')
        serializer = DemoVoteResponseSerializer(teamlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

