from rest_framework import serializers

from chat.models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'receiver', 'created', 'accepted', 'sender']

    def get_receiver(self, obj):
        return obj.receiver.last_name, obj.receiver.first_name, obj.receiver.id

    def get_sender(self, obj):
        return obj.sender.last_name, obj.sender.first_name, obj.sender.id


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'created', 'text', 'conversation']

    def get_user(self, obj):
        return obj.user.first_name, obj.user.last_name, obj.user.id
