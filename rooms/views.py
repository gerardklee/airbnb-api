from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer

# class view of http methods
class RoomsView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serialized_rooms = RoomSerializer(results, many=True, context={'request': request})
        #return Response(serialized_rooms.data)
        return paginator.get_paginated_response(serialized_rooms.data)

    def post(self, request):
        # Authenticate is NOT required for this project
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: find out about save(user=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleRoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        serialized_room = RoomSerializer(room).data

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if room is not None:
            room.delete()
            return Response(data=serialized_room, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=RoomSerializer(room).data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get('max_price', None)
    min_price = request.GET.get('min_price', None)
    beds      = request.GET.get('beds', None)
    bedrooms  = request.GET.get('bedrooms', None)
    bathrooms = request.GET.get('bathrooms', None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs['price__lte'] = max_price
    if min_price is not None:
        filter_kwargs['price__gte'] = min_price
    if beds is not None:
        filter_kwargs['beds__lte'] = beds
    if bedrooms is not None:
        filter_kwargs['bedrooms__gte'] = bedrooms
    if bathrooms is not None:
        filter_kwargs['bathrooms__gte'] = bathrooms
    paginator = PageNumberPagination()
    paginator.page_size = 10
    rooms = Room.objects.filter(**filter_kwargs)
    results = paginator.paginate_queryset(rooms, request)
    serialized_rooms = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serialized_rooms.data)


# functional view of http methods
# function below is not being used
@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)   

    elif request.method == "POST":
        # authenticate
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)










