from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model() 

class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model
    """
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    participants_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'participants_usernames', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_participants_usernames(self, obj):
        """
        Returns a list of usernames of the Chat participants
        """
        return [user.username for user in obj.participants.all()]

    def create(self, validated_data):
        """
        Overrides the create method to handle the ManyToManyField 'participants'
        """
        participants_data = validated_data.pop('participants', [])
        chat = Chat.objects.create(**validated_data)
        chat.participants.set(participants_data)
        return chat

    def update(self, instance, validated_data):
        """
        Overrides the update method to handle the ManyToManyField 'participants'
        """
        participants_data = validated_data.pop('participants', None)
        if participants_data is not None:
            instance.participants.set(participants_data)  # Updates the participants

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MensagemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Mensagem model
    Includes the sender's username
    """
    sender_username = serializers.ReadOnlyField(source='sender.username')
    # The 'chat' field will be a Chat ID (Writable Nested Serializer or PrimaryKeyRelatedField)
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    # The 'sender' field will be a user ID (Writable Nested Serializer or PrimaryKeyRelatedField)
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    exchange_confirmed_by_username = serializers.ReadOnlyField(source='exchange_confirmed_by.username')
    location_confirmed_by_username = serializers.ReadOnlyField(source='location_confirmed_by.username')

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'sender_username', 'timestamp', 
            'message_type', 'text_content', 'location_data', 'suggestion_data',
            'exchange_confirmed', 'exchange_confirmed_by', 'exchange_confirmed_by_username',
            'location_confirmed', 'location_confirmed_by', 'location_confirmed_by_username', 
        ]
        read_only_fields = ['timestamp', 'exchange_confirmed_by', 'location_confirmed_by'] 

    def validate(self, data):
        """
        Validates that only the relevant field for the message_type is filled in.
        """
        message_type = data.get('message_type', 'text')
        text_content = data.get('text_content')
        location_data = data.get('location_data')
        suggestion_data = data.get('suggestion_data')

        if message_type == 'text':
            if not text_content:
                raise serializers.ValidationError("Messages of type 'text' must have 'text_content'.")
            if location_data or suggestion_data:
                raise serializers.ValidationError("Messages of type 'text' must not have 'location_data' or 'suggestion_data'.")
        elif message_type == 'location':
            if not location_data:
                raise serializers.ValidationError("Messages of type 'location exchange' must have 'location_data'.")
            if text_content or suggestion_data:
                raise serializers.ValidationError("Messages of type 'location exchange' must not have 'text_content' or 'suggestion_data'.")
        elif message_type == 'suggestion':
            if not suggestion_data:
                raise serializers.ValidationError("Messages of type 'exchange suggestion' must have 'suggestion_data'.")
            if text_content or location_data:
                raise serializers.ValidationError("Messages of type 'exchange suggestion' must not have 'text_content' or 'location_data'.")
        else:
            raise serializers.ValidationError("Invalid message type.")

        return data
