from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from models import User
from serializers import RegisterSerializer, UserSerializer


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['loginId']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        # ID가 존재하지 않는 경우
        if user is None:
            return Response(
                {"message": "회원정보가 일치하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

        # # 비밀번호가 틀린 경우
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면,
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열화
            access_token = str(token.access_token)  # access 토큰 문자열화
            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            # response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class SignOut(APIView):
    def post(self, request):
        response = Response({
            "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
        # response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class IDCheck(APIView):
    def post(self, request):

        if User.objects.filter(login_id=request.data['loginId']).exists():
            response = Response(
                {"message": "중복된 아이디가 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        else:
            response = Response(status=status.HTTP_200_OK)

        return response


class EmailCheck(APIView):
    def post(self, request):

        if User.objects.filter(email=request.data['email']).exists():
            response = Response(
                {"message": "중복된 이메일이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        else:
            response = Response(status=status.HTTP_200_OK)

        return response
