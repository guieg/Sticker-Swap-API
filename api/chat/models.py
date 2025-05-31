from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Chat(models.Model):
    """
    Represents a Chat between multiple users (participants)
    """
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ['-updated_at']

    def __str__(self):
        participants_names = ", ".join([user.username for user in self.participants.all()])
        return f"Chat with {participants_names}"

class Message(models.Model):
    """
    Represents a message within a Chat
    """
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('location', 'Exchange Location'),
        ('suggestion', 'Exchange Suggestion'),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    text_content = models.TextField(blank=True, null=True)
    location_data = models.TextField(blank=True, null=True)
    suggestion_data = models.TextField(blank=True, null=True)

    # Indica se a troca de figurinhas foi confirmada
    exchange_confirmed = models.BooleanField(
        default=False,
        null=True
    )
    # Quem confirmou a troca de figurinhas (opcional, pode ser nulo se não confirmada)
    exchange_confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Mantém a mensagem se o usuário for deletado
        related_name='confirmed_exchanges',
        null=True,
        blank=True,
    )

    location_confirmed = models.BooleanField(
        default=False,
        null=True,
        help_text="Indica se o local de troca nesta mensagem foi confirmado."
    )
    location_confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Mantém a mensagem se o usuário for deletado
        related_name='confirmed_locations',
        null=True,
        blank=True,
        help_text="O usuário que confirmou o local de troca."
    )   

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in Chat {self.chat.id} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
