from django.shortcuts import render
from .serializers import ChatSerializer, MensagemSerializer
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

        # @action(detail=True, methods=['get'], url_path='mensagens')
    def listar_mensagens(self, request, pk=None):
        """
        Lista todas as mensagens pertencentes a esta conversa (Chat).
        """
        try:
            chat = self.get_object() # Obtém o objeto Chat pelo PK
        except Chat.DoesNotExist:
            return Response({"detail": "Conversa não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        mensagens = Message.objects.filter(chat=chat).order_by('timestamp')
        serializer = MensagemSerializer(mensagens, many=True)
        
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
    
    @action(detail=True, methods=['put'], url_path='confirmar-troca')
    def confirm_exchange(self, request, pk=None):
        """
        Confirma a sugestão de troca contida em uma mensagem.
        Endpoint: PUT /api/chat/mensagens/{id}/confirmar-troca/
        """
        try:
            message = self.get_object() # Obtém a mensagem pelo PK
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Verifica se a mensagem é do tipo 'suggestion'
        if message.message_type != 'suggestion':
            return Response(
                {"detail": "Esta mensagem não é uma sugestão de troca e não pode ser confirmada como tal."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user not in message.chat.participants.all():
            return Response(
                {"detail": "Você não tem permissão para confirmar esta troca."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.exchange_confirmed = True
        message.exchange_confirmed_by = request.user # Define quem confirmou
        message.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='confirmar-local')
    def confirm_location(self, request, pk=None):
        """
        Confirma o local de troca contido em uma mensagem.
        Endpoint: PUT /api/chat/mensagens/{id}/confirmar-local/
        """
        try:
            message = self.get_object() # Obtém a mensagem pelo PK
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Verifica se a mensagem é do tipo 'location'
        if message.message_type != 'location':
            return Response(
                {"detail": "Esta mensagem não é um local de troca e não pode ser confirmada como tal."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se o usuário logado é um dos participantes da conversa
        if request.user not in message.chat.participants.all():
            return Response(
                {"detail": "Você não tem permissão para confirmar este local de troca."},
                status=status.HTTP_403_FORBIDDEN
            )

        message.location_confirmed = True
        message.location_confirmed_by = request.user # Define quem confirmou
        message.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
