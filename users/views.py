from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReadUserSerializer, ReadFavSerializer, WriteUserSerializer
from .models import User
from rooms.serializers import RoomSerializer
from rooms.models import Room

class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        users_serializer = ReadUserSerializer(users, many=True)
        return Response(data=users_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.data
        user_serializer = WriteUserSerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    def get(self, request):
        my_serializer = ReadUserSerializer(request.user).data
        if request.user.is_authenticated:
            return Response(data=my_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: this has to handle some exceptions
    def put(self, request):
        return Response(status=status.HTTP_200_OK)

@api_view(["GET", "PUT"])
def user_view(request, pk):
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

@api_view(["GET", "PUT"])
def toggle_fav(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if request.method == "GET":
            fav_rooms_serializer = RoomSerializer(user.favs.all(), many=True)
            return Response(data=fav_rooms_serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            room_id = request.data.get("id", None)
            try:
                room = Room.objects.get(pk=room_id)
                room_serializer = RoomSerializer(room)
                user.favs.add(room)
                user.save()
                return Response(data=room_serializer.data, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
