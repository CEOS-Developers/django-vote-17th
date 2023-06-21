from poll.models import Poll, Vote
from poll.serializers import PollSerializer, VoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class PollAPIView(APIView):

    @staticmethod
    def get(request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        print(serializer.data)
        return Response(serializer.data)


"""
PollResultAPIView : 투표 결과를 가져오는 APIView
Vote를 가져올 때 Poll의 pk를 이용해서 가져온다.
"""
class PollResultAPIView(APIView):

    @staticmethod
    def get(request, poll_type):
        if poll_type == 'part-leader':
            pk = 1
        elif poll_type == 'demo':
            pk = 0
        votes = Vote.objects.filter(poll=pk)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)


'''
참고하려고 가져왔음 무시해도됨
class PostList(APIView):

        @staticmethod
        def get(request):
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

        @staticmethod
        def post(request):

            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)

            return Response(serializer.errors, status=400)
        
        
'''