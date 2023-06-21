from poll.models import Poll, Vote
from poll.serializers import PollSerializer, VoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Team
from account.serializers import TeamSerializer


class PollAPIView(APIView):

    @staticmethod
    def get(request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        print(serializer.data)
        return Response(serializer.data)


class DemoVoteAPIView(APIView):
    """
    DemoVoteAPIView : 투표를 하는 APIView

    POST /polls/vote/demo/ : 투표를 한다
    GET /polls/vote/demo/ : 투표 선택지(팀 명단)을 불러온다
    """
    @staticmethod
    def post(request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @staticmethod
    def get(request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)






class DemoResultAPIView(APIView):
    """
    DemoResultAPIView : 투표 결과를 가져오는 APIView
    Vote를 가져올 때 Poll의 pk를 이용해서 가져온다.
    """
    @staticmethod
    def get(request):
        votes = Vote.objects.filter(poll=1)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)


# TODO : PartLeaderAPIView 구현
