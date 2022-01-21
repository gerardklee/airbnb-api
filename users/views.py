from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User

class MeView(APIView):
    def get(self, request):
        my_serializer = ReadUserSerializer(request.user).data
        if request.user.is_authenticated:
            return Response(data=my_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        print("me_view")
        return Response(status=status.HTTP_200_OK)

@api_view(["GET", "PUT"])
def user_view(request, pk):
    print("user_view")
    try:
        user = User.objects.get(pk=pk)
        if request.method == "GET":
            user_serializer = ReadUserSerializer(user)
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            user_serializer = WriteUserSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(data=user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
