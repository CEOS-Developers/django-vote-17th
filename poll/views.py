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


class PollResultAPIView(APIView):

    @staticmethod
    def get(request, pk):
        votes = Vote.objects.filter(poll=pk)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)


'''

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