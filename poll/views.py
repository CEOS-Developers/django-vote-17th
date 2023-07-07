from poll.models import Poll, Vote
from poll.serializers import PollSerializer, VoteGetSerializer, VotePostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Team, User
from account.serializers import UserSerializer, TeamSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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

    POST /polls/vote/demo/ : 투표를 한다 **토큰 인증 필요**
    GET /polls/vote/demo/ : 투표 선택지(팀 명단)을 불러온다
    """
    permission_classes = (IsAuthenticated,)


    @staticmethod
    def post(request):
        poll = Poll.objects.get(name="데모데이 투표")
        voter = User.objects.get(username=request.data.get('voter'))
        target_team = Team.objects.get(name=request.data.get('target_team'))

        temp = request.data.copy()
        print(temp)
        temp['poll'] = poll.pk
        temp['voter'] = voter.pk
        temp['target_team'] = target_team.pk
        print(temp.get('target_account'))
        print(temp)
        serializer = VotePostSerializer(data=temp)
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
        print("demo")
        teams = Team.objects.all()
        votes = Vote.objects.filter(poll__name="데모데이 투표")
        arr = []
        for each in teams:
            arr.append([each.name, len(votes.filter(target_team__name=each.name))])
        return Response(arr)


# TODO : PartLeaderAPIView 구현
class PartLeaderVoteAPIView(APIView):
    """
    PartLeaderAPIView : 투표를 하는 APIView

    GET /polls/vote/part-leader/front-end
    GET /polls/vote/part-leader/back-end
    >> 각각 맞는 파트 인원들을 불러옴

    POST /polls/vote/part-leader/front-end
    POST /polls/vote/part-leader/back-end
    >> 투표하기
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, part):
        if part == "front-end":
            users = User.objects.filter(part__name="Frontend")
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif part == "back-end":
            users = User.objects.filter(part__name="Backend")
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)

    @staticmethod
    def post(request, part):

        poll = Poll.objects.get(name="파트장 투표").pk
        voter = User.objects.get(username=request.data.get('voter')).pk
        target_account = User.objects.get(username=request.data.get('target_account')).pk

        temp = request.data.copy()
        temp['target_account'] = target_account
        temp['poll'] = poll
        temp['voter'] = voter

        serializer = VotePostSerializer(data=temp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class PartLeaderResultAPIView(APIView):
    """
    GET /polls/part-leader/front-end
    GET /polls/part-leader/back-end

    PartLeaderResultAPIView : 투표 결과를 가져오는 APIView
    Vote를 가져올 때 Poll의 pk를 이용해서 가져온다.
    """
    @staticmethod
    def get(request, part):
        if part == "front-end":
            print("front-end")
            # 프론트엔드 유저 가져옴
            users = User.objects.filter(part__name="Frontend")
            votes = Vote.objects.filter(poll__name="파트장 투표")
            # 투표자 중 front-end 파트인 사람들만 가져옴
            votes = votes.filter(target_account__part__name="Frontend")
            arr = []
            for each in users:
                arr.append([each.username, each.team.name, len(votes.filter(target_account__username=each.username))])
            return Response(arr)
        elif part == "back-end":
            print("back-end")
            # 프론트엔드 유저 가져옴
            users = User.objects.filter(part__name="Backend")
            votes = Vote.objects.filter(poll__name="파트장 투표")
            # 투표자 중 front-end 파트인 사람들만 가져옴
            votes = votes.filter(target_account__part__name="Backend")
            arr = []
            for each in users:
                arr.append([each.username, each.team.name, len(votes.filter(target_account__username=each.username))])
            return Response(arr)
        else:
            return Response(status=400)

class CheckVoteAPIView(APIView):
    @staticmethod
    def get(request, userid):
        try:
            # 파트장 투표 여부
            has_voted_part = Vote.objects.filter(voter__userid=userid, poll__name="파트장 투표").exists()
            # 데모데이 투표 여부
            has_voted_demo = Vote.objects.filter(voter__userid=userid, poll__name="데모데이 투표").exists()

            res = Response(
                {
                    "has_voted_part": has_voted_part,
                    "has_voted_demo": has_voted_demo,
                },
                status=status.HTTP_200_OK
            )
            return res
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
