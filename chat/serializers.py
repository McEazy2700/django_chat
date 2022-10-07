from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        description = "Chat message Instance"
        fields = ["id", "sender", "content", "date_added"]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["message", "receiver", "date_created", "last_updated"]
