from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Profile


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, max_length=255, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=255, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance: User, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.username = validated_data.get("title", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            # "first_name",
            # "last_name",
        )
        extra_kwargs = {"username": {"required": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields did not match"}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            # first_name=validated_data["first_name"],
            # last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "profile_picture"]
