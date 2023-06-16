import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,SignUpSerializer,LoginSerializer
from django_vote_17th.settings import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY
from .models import User
from django.contrib.auth import get_user_model


class SignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):

            user_id = serializer.validated_data.get('user_id') # 아이디 불러옴
            if User.objects.filter(user_id=user_id).exists():
                return Response({"message": "아이디가 중복됩니다."}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data.get('email') # 이메일 불러옴
            if User.objects.filter(email=email).exists():
                return Response({"message": "이메일이 중복됩니다."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(request)
            response = Response(
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "part":user.part,
                    "name":user.name,
                    "team":user.team,
                },
                status=status.HTTP_200_OK,
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효성 검사 실패 시 예외 발생

        # 유효성 검사를 통과한 경우 validated_data에서 값을 가져옴
        user_id = serializer.validated_data.get("user_id")
        access_token = serializer.validated_data.get("access_token")

        response = Response({
            "user_id": user_id,
            "token": {
                "access_token": access_token,
            }},
            status=status.HTTP_200_OK,
        )

        # 쿠키에 삽입 후 프론트로 전달
        response.set_cookie("access_token", access_token, httponly=True, secure=True, max_age=60 * 60 * 3)  # 만료 3시간

        return response



class LogoutView(APIView):

    #로그아웃시 jwt토큰 삭제
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        return response



class AuthView(APIView):
    def get(self, request):
        #access token을 프론트가 보낸 request에서 추출
        print(request)
        access_token = request.META['HTTP_AUTHORIZATION'].split()[1]
        print(access_token)
        #access token이 없다면 에러 발생
        if not access_token:
            return Response({"message": "access token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

        #access token이 있다면
        #토큰 디코딩(유저 식별)
        try:
            #payload에서 user_id(고유한 식별자)를 추출
            #payload={'user_id:1'}

            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) #accesstoken 번호
            user_id = payload.get('user_id') #1로 넣었는데 5가 나옴
            print(user_id) #5
            #해당 유저 아이디를 가지는 객체 user을 가져와
            user = get_object_or_404(User, id=user_id) #id=5인 애를 가져와야 됨
            #UserSerializer로 JSON화 시켜준 뒤,
            serializer = UserSerializer(instance=user)
            #프론트로 200과 함께 재전송
            return Response(serializer.data, status=status.HTTP_200_OK)

         #Access token 예
        except jwt.exceptions.InvalidSignatureError:
            #access_token 유효하지 않음
            return Response({"message": "유효하지 않은 access token"}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.ExpiredSignatureError:
            # access_token 만료 기간 다 됨
            refresh_token = request.COOKIES.get('refresh_token')

            #refresh_token이 없다면 에러 발생
            if not refresh_token:
                return Response({"message": "refresh token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                #refresh_token 디코딩
                payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                user = get_object_or_404(id=user_id)

                #새로운 access_token 발급
                access_token = jwt.encode({"user_id": user.pk}, SECRET_KEY, algorithm=['HS256'])

                #access_token을 쿠키에 저장하여 프론트로 전송
                response = Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)
                response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='None', secure=True)

                return response

            # refresh_token 예외 처리
            except jwt.exceptions.InvalidSignatureError:
                # refresh_token 유효하지 않음
                return Response({"message": "유효하지 않은 refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

            except jwt.exceptions.ExpiredSignatureError:
                # refresh_token 만료 기간 다 됨 => 이경우에는, 사용자가 로그아웃 후 재로그인하도록 유인 => 리다이렉트
                return Response({"message": "refresh token 기간 만료"}, status=status.HTTP_401_UNAUTHORIZED)
