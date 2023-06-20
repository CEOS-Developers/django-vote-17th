
from django_filters import exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from account.views import AuthView
from vote.serializers import *



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team



class TeamVoteView(APIView):

    def get(self, request):
        team_list = Team.objects.all().order_by('-vote_cnt').values()
        serializer = TeamSerializer(team_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        if AuthView.get(self, request).status_code is status.HTTP_200_OK:
            login_user = AuthView.get(self, request).data
            login_user_detail = User.objects.get(user_id=login_user['user_id'])

            if login_user_detail is not None:
                serializer = TeamVoteSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    vote = serializer.save()  # 투표해서 저장
                    team_name = serializer.validated_data.get("team")  # 투표한 팀 가져옴
                    user_name = serializer.validated_data.get("user_name")  # 투표자 가져옴
                    try:
                        team = Team.objects.get(team=team_name)  # 해당 팀 가져옴
                        user = User.objects.get(name=user_name)
                        if user.is_teamvote:
                            response_data = {
                                "error": "팀 투표를 이미 하셨습니다."
                            }
                            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                        team.vote_cnt += 1  # 팀 투표 수 증가
                        team.save()
                        user.is_teamvote = True
                        user.save()
                        response_data = {
                            "user_name": vote.user_name,
                            "team": team.team,
                            "team_cnt": team.vote_cnt
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    except Team.DoesNotExist:
                        response_data = {
                            "error": f"The team '{team_name}' does not exist."
                        }
                        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif AuthView.get(self, request).status_code is status.HTTP_400_BAD_REQUEST:
                raise exceptions.ValidationError(detail='Please login for voting')

            elif AuthView.get(self, request).status_code is status.HTTP_401_UNAUTHORIZED:
                raise exceptions.ValidationError(detail='token is expired')

            elif AuthView.get(self, request).status_code is status.HTTP_403_FORBIDDEN:
                raise exceptions.ValidationError(detail='Please login again')


class CandidateVoteView(APIView):
    def get(self, request, part):
        candidate_list = Candidate.objects.filter(part=part).order_by('-vote_cnt')
        serializer = CandidateSerializer(candidate_list, many=True)
        return Response(serializer.data)

    def post(self, request, part):
        if AuthView.get(self, request).status_code is status.HTTP_200_OK:
            login_user = AuthView.get(self, request).data
            login_user_detail = User.objects.get(user_id=login_user['user_id'])

            if login_user_detail is not None:
                serializer = CandidateVoteSerializer(data=request.data)

                if serializer.is_valid(raise_exception=False):
                    vote = serializer.save()  # 투표해서 저장
                    candidate_name = serializer.validated_data.get("candidate")  # 투표한 파트장 후보 가져옴
                    user_name = serializer.validated_data.get("user_name")  # 투표자 가져옴
                    try:
                        candidate = Candidate.objects.get(name=candidate_name)
                        user = User.objects.get(name=user_name)
                        if user.is_partvote:
                            response_data = {
                                "error": "파트장 투표를 이미 하셨습니다."
                            }
                            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                        candidate.vote_cnt += 1  # 팀 투표 수 증가
                        candidate.save()
                        user.is_partvote = True
                        user.save()
                        response_data = {
                           "user_name": vote.user_name,
                           "team": candidate.name,
                           "team_cnt": candidate.vote_cnt
                         }
                        return Response(response_data, status=status.HTTP_200_OK)
                    except Candidate.DoesNotExist:
                      response_data = {
                        "error": f"The team '{candidate_name}' does not exist."
                      }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif AuthView.get(self, request).status_code is status.HTTP_400_BAD_REQUEST:
            raise exceptions.ValidationError(detail='Please login for voting')

        elif AuthView.get(self, request).status_code is status.HTTP_401_UNAUTHORIZED:
            raise exceptions.ValidationError(detail='token is expired')

        elif AuthView.get(self, request).status_code is status.HTTP_403_FORBIDDEN:
            raise exceptions.ValidationError(detail='Please login again')

