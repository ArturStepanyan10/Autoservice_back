from rest_framework import serializers

from chat.models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(source='receiver.last_name', read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'receiver', 'created', 'accepted']


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'created', 'text', 'conversation']
