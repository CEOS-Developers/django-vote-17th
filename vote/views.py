from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from vote.serializers import TeamVoteSerializer, CandidateVoteSerializer
from rest_framework.views import APIView
from account.models import *
from vote.models import *
from rest_framework.response import Response


class TeamVoteView(APIView):
    def post(self, request):
        user_id = request.data.get('userPk')
        team_id = request.data.get('teamPk')
        user = User.objects.get(id=user_id)
        team = Team.objects.get(id=team_id)

        team_vote_serializer = TeamVoteSerializer(data={
            'userPk': user_id,
            'teamPk': team_id
        })

        if team_vote_serializer.is_valid():
            team_vote_serializer.save()
            team.count += 1
            team.save()
            return JsonResponse({'message': 'Team vote created.'}, status=200)

        return JsonResponse({'message': 'Failed to create team vote.'}, status=400)


class CandidateVoteView(CreateAPIView):
    queryset = CandidateVote.objects.all()
    serializer_class = CandidateVoteSerializer