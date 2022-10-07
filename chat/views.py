from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import MessageSerializer, ChatSerializer
from .models import Message, Chat

# Create your views here.


class MessageGetAndCreateView(APIView, LoginRequiredMixin):
    """
    Get and Create view for message.
    """
    def perform_create(self, serializer:MessageSerializer):
        serializer.save(sender=self.request.user)

    def get(
        self,
        request: Request,
        format=None,
    ):
        """Return a chat message instance."""
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, format=None):
        """Creates and returns a message instance."""
        if not request.user.is_authenticated:
            return Response({"error": "User must be authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetailView(APIView, LoginRequiredMixin):
    """
    Detail, Delete, and Update Message view.
    """
    def get_message(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request:Request, pk):
        message = self.get_message(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request:Request, pk):
        message = self.get_message(pk=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=message, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
