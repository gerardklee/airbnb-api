from rest_framework import serializers
from .models import User

# Below class is used in rooms serializer for relation-purposes
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups", 
            "user_permissions", 
            "password", 
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "favs"
        )

class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups", 
            "user_permissions", 
            "password", 
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "favs"
        )