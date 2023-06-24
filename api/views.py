from django.shortcuts import render
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CandidateVoteAPIView(APIView):

    def post(self, request):
        serializer = CandidateVoteRequestSerializer(data=request.data)
        # User의 isCandiVoted = 0 이면
        if 0 == 0:
            cname = request.data['cname']
            candidate = Candidate.objects.get(cname=cname)
            candidate.count = candidate.count + 1
            candidate.save()
            # User의 isCandiVote 값 변경해주기
            # request.user.isCandiVoted = 1
            res = Response(
                {
                    "isSuccess": "true",
                    "code": 200
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response({
                    "isSuccess": "false",
                    "code": 400,
                    "message": "접근 권한이 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)


class FEVoteResultAPIView(APIView):
    def get(self, request):
        candidatelist = Candidate.objects.filter(part='fe').order_by('-count')
        serializer = CandidateVoteResponseSerializer(candidatelist, many=True)
        return Response(serializer.data)


class BEVoteResultAPIView(APIView):
    def get(self, request):
        candidatelist = Candidate.objects.filter(part='be').order_by('-count')
        serializer = CandidateVoteResponseSerializer(candidatelist, many=True)
        return Response(serializer.data)


class DemoVoteAPIView(APIView):
    def post(self, request):
        serializer = DemoVoteRequestSerializer(data=request.data)
        # User의 isDemoVoted = 0 이면
        if 0 == 0:
            tname = request.data['tname']
            team = Team.objects.get(tname=tname)
            team.count = team.count + 1
            team.save()
            # User의 isCandiVote 값 변경해주기
            # request.user.isCandiVoted = 1
            res = Response(
                {
                    "isSuccess": "true",
                    "code": 200
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response({
                "isSuccess": "false",
                "code": 400,
                "message": "접근 권한이 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)


class DemoVoteResultAPIView(APIView):
    def get(self, request):
        teamlist = Team.objects.all().order_by('-count')
        serializer = DemoVoteResponseSerializer(teamlist, many=True)
        return Response(serializer.data)
