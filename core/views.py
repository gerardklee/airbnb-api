from django.core import serializers
from django.http import HttpResponse
from rooms.models import Room

def list_rooms(request):
	rooms = Room.objects.all()
	rooms_json = serializers.serialize("json", rooms)
	response = HttpResponse(content=rooms_json)
	return response

def test(request):
	pass