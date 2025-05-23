from django.db import models
from django.conf import settings
from api.accounts.models import User

class Chat(models.Model):
    """
    Represents a Chat between users
    Relates to User and Messages
    """
    # Many-to-many relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ['-updated_at'] # Orders the conversations by the most recent

    def __str__(self):
        # Returns a readable representation of the Chat
        # Ex: "Chat with User1, User2..."
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

    # One-to-many relationship with Chat (a message belongs to a Chat)
    Chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')

    # One-to-many relationship with User (a sender for the message)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10,choices=MESSAGE_TYPE_CHOICES,default='text')
    text_content = models.TextField(blank=True,null=True)
    location_data = models.TextField(blank=True,null=True)
    suggestion_data = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp'] # Orders the messages by the sending time

    def __str__(self):
        return f"Message from {self.sender.username} in Chat {self.Chat.id} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"