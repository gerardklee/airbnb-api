from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReadUserSerializer

class MeView(APIView):
    def get(self, request):
        my_serializer = ReadUserSerializer(request.user).data
        if request.user.is_authenticated:
            return Response(data=my_serializer, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        pass

@api_view(["GET"])
def user_view(request, pk):
    if request.method == "GET":
        return Response({"message":"GET request received"})
    pass