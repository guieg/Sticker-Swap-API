from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from .models import Chat, Message
from .serializers import ChatSerializer, MensagemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ChatViewSet(viewsets.ModelViewSet):
    """
    View to list, create, retrieve, update, and delete chat conversations
    Only authenticated users are allowed access
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """
        Filters chats to show only those where the logged-in user is a participant
        """
        return Chat.objects.filter(participants=self.request.user) 
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_chats_by_user(self, request, user_id=None):
        """
        Customized endpoint to list Chats from user
        """
        chats = Chat.objects.filter(participants__id=user_id)
        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data)        

class MensagemViewSet(viewsets.ModelViewSet):
    """
    View to list, create, retrieve, update, and delete messages
    """
    queryset = Message.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authentication

    def perform_create(self, serializer):
        """
        Automatically sets the sender of the message as the logged-in user
        """
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_messages_by_user(self, request, user_id=None):
        """
        Customized endpoint to list messages by user
        """
        messages = Message.objects.filter(sender__id=user_id)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
