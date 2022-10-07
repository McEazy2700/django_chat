from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, unique=True, max_length=255)
    email = serializers.EmailField(required=True, unique=True,)
    first_name = serializers.CharField(required=False, max_length=255, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=255, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance:User, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.username = validated_data.get('title', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture']
