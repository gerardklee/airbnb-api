from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

# functional view of http methods
@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)   
    elif request.method == "POST":
        # authenticate
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

# class view of http methods
class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized_rooms = ReadRoomSerializer(rooms, many=True)
        return Response(serialized_rooms.data)
    def post(self, request):
        # Authenticate is NOT required for this project
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer