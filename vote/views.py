from rest_framework import status
from rest_framework.views import APIView
from account.models import *
from vote.models import *
from rest_framework.response import Response

from vote.serializers import TeamVoteSerializer, CandidateVoteSerializer, TeamSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team


class TeamVoteView(APIView):
    def post(self, request):
        serializer = TeamVoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            vote = serializer.save()  # 투표해서 저장
            team_name = serializer.validated_data.get("team")  # 투표한 팀 가져옴
            try:
                team = Team.objects.get(team=team_name)  # 해당 팀 가져옴
                team.vote_cnt += 1  # 팀 투표 수 증가
                team.save()
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


class CandidateVoteView(APIView):
    def post(self, request):
        serializer = CandidateVoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            vote = serializer.save(request)  # 투표해서 저장
            name = serializer.validated_data.get("name")  # 투표한 파트장 가져옴
            if Candidate.object.filter(name=name).exists():  # 데베에 해당 파트장이 있다면
                candidate = Candidate.objects.get(name=name)  # 후킹팀에
                vote_cnt=candidate.vote_cnt  # 파트장 투표
                vote_cnt += 1
                candidate.save()
            response = Response(
                {
                    "user_id": vote.user_id,
                    "candidate":vote.candidate
                },
                status=status.HTTP_200_OK,
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
