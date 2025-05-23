from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MensagemSerializer

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
