from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from polls.models import teamPoll, partPoll
from .serializers import TeamPollSerializer, PartPollSerializer

@api_view(['GET'])
def team_poll_list(request):
    team_polls = teamPoll.objects.order_by('-voteCnt')
    serializer = TeamPollSerializer(team_polls, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def team_poll_vote(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'detail': 'You must be logged in to vote.'}, status=status.HTTP_401_UNAUTHORIZED)

    part = user.part
    serializer = TeamPollSerializer(data=request.data)
    if serializer.is_valid():
        team_id = serializer.validated_data['team']
        team_poll = get_object_or_404(teamPoll, team=team_id)
        if team_poll.userId != part:
            return Response({'detail': 'You can only vote for your own part.'}, status=status.HTTP_403_FORBIDDEN)

        team_poll.voteCnt += 1
        team_poll.save()
        return Response({'detail': 'Vote successful.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def part_poll_list(request):
    part_polls = partPoll.objects.order_by('-voteCnt')
    serializer = PartPollSerializer(part_polls, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def part_poll_vote(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'detail': 'You must be logged in to vote.'}, status=status.HTTP_401_UNAUTHORIZED)

    team = user.team
    serializer = PartPollSerializer(data=request.data)
    if serializer.is_valid():
        candidate_id = serializer.validated_data['candidate']
        candidate_poll = get_object_or_404(partPoll, candidate=candidate_id)
        if candidate_poll.userId.team == team:
            return Response({'detail': 'You cannot vote for your own team.'}, status=status.HTTP_403_FORBIDDEN)

        candidate_poll.voteCnt += 1
        candidate_poll.save()
        return Response({'detail': 'Vote successful.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
