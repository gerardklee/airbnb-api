from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer

class RoomsList(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True)
        return Response(serialized_rooms.data)

@api_view(["GET"])
def list_rooms(request):
    return Response()