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

class WriteUserSerializer(serializers.Serializer):
    username   = serializers.CharField(max_length=140)
    first_name = serializers.CharField(max_length=140)
    last_name  = serializers.CharField(max_length=140)
    email      = serializers.EmailField(max_length=254)

    def valiate(self, data):
        print("data in validated: ", data)
        return data

    def update(self, instance, validated_data):
        print("instance in update: ", instance)
        print("data in validated_data: ", validated_data)
        instance.username   = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name  = validated_data.get("last_name", instance.last_name)
        instance.email      = validated_data.get("email", instance.email)
        instance.save()
        return instance
