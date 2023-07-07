from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from .models import *
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import *
from django.db.models import Count
from accounts.serializers import *
# Create your views here.

class TeamVoteView(APIView):

    def get(self, request, format=None):
        vote = Team_Vote.objects.all()
        serializer = TeamVoteSerializer(vote, many=True)
        vote_count = Team_Vote.objects.filter().values('team').annotate(total=Count('team')).order_by('-total')
        return Response({'message': "투표 조회", 'vote_count':vote_count, 'data': serializer.data}, status=HTTP_200_OK)

    # def post(self, request, format=None):
    #     user = self.request.user
    #     serializer=TeamVoteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         if Team_Vote.objects.filter(user=user, team=serializer.validated_data['team']):
    #             delete_vote = Team_Vote.objects.get(user=user, team=serializer.validated_data['team'])
    #             delete_vote.delete()
    #             return Response({'message': '투표 취소', 'data': serializer.data}, status=HTTP_201_CREATED)
    #         else:
    #             if user.team==serializer.validated_data['team']:
    #                 return Response({'message': '내 팀은 투표 할 수 없습니다!', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    #             else:
    #                 serializer.save(user=self.request.user, team=serializer.validated_data['team'])
    #                 return Response({'message':'투표 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
    #     return Response({'message': '투표 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        user = self.request.user
        serializer = TeamVoteSerializer(data=request.data)
        if serializer.is_valid():
            # if Team_Vote.objects.filter(user=user, team=serializer.validated_data['team']):
            #     user_update = get_object_or_404(User, name=user.name)
            #     user_update.team_vote = False
            #     user_update.save()
            #     delete_vote = Team_Vote.objects.get(user=user, team=serializer.validated_data['team'])
            #     delete_vote.delete()
            #     return Response({'message': '투표 취소', 'data': serializer.data, 'user':user_update.team_vote}, status=HTTP_201_CREATED)
            # else:
            #     if user.team == serializer.validated_data['team']:
            #         return Response({'message': '내 팀은 투표 할 수 없습니다!', 'data': serializer.errors},
            #                         status=HTTP_400_BAD_REQUEST)
            #     elif Team_Vote.objects.filter(user=user):
            #         return Response({'message': '투표는 한 번만!', 'data': serializer.errors},
            #                         status=HTTP_400_BAD_REQUEST)
            #     else:
            #         user_update=get_object_or_404(User, name=user.name)
            #         user_update.team_vote=True
            #         user_update.save()
            #         serializer.save(user=self.request.user, team=serializer.validated_data['team'])
            #         return Response({'message': '투표 성공', 'data': serializer.data, 'user':user_update.team_vote}, status=HTTP_201_CREATED)
            if user.team == serializer.validated_data['team']:
                return Response({'message': '내 팀은 투표 할 수 없습니다!', 'data': serializer.errors},
                                status=HTTP_400_BAD_REQUEST)
            elif Team_Vote.objects.filter(user=user):
                return Response({'message': '투표는 한 번만!', 'data': serializer.errors},
                                status=HTTP_400_BAD_REQUEST)
            else:
                user_update=get_object_or_404(User, name=user.name)
                user_update.team_vote=True
                user_update.save()
                serializer.save(user=self.request.user, team=serializer.validated_data['team'])
                return Response({'message': '투표 성공', 'data': serializer.data, 'user':user_update.team_vote}, status=HTTP_201_CREATED)
        return Response({'message': '투표 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)





class PartVoteView(APIView):
    def get(self, request, format=None):
        vote = Part_Vote.objects.all()
        serializer = PartVoteSerializer(vote, many=True)
        vote_count = Part_Vote.objects.filter().values('part').annotate(total=Count('part')).order_by('-total')

        return Response({'message': "투표 조회", 'vote_count':vote_count, 'data': serializer.data}, status=HTTP_200_OK)

    def post(self, request, format=None):
        user = self.request.user
        serializer=PartVoteSerializer(data=request.data)
        if serializer.is_valid():
            if Part_Vote.objects.filter(user=user, part=serializer.validated_data['part']):
                user_update = get_object_or_404(User, name=user.name)
                user_update.part_vote = False
                user_update.save()
                delete_vote = Part_Vote.objects.get(user=user, part=serializer.validated_data['part'])
                delete_vote.delete()
                return Response({'message': '투표 취소', 'data': serializer.data,'user': user_update.part_vote}, status=HTTP_201_CREATED)
            else:
                user_update = get_object_or_404(User, name=user.name)
                user_update.part_vote = True
                user_update.save()
                serializer.save(user=self.request.user, part=serializer.validated_data['part'])
                return Response({'message':'투표 성공', 'data': serializer.data,'user': user_update.part_vote}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


