from asgiref.sync import sync_to_async
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action

from chat.models import Conversation, Message
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncAPIConsumer):

    async def connect(self):
        """Подключение пользователя к WebSocket-комнате"""
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Отключение пользователя"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @action()
    async def send_message(self, message, user_id, **kwargs):
        """Метод для отправки сообщений"""
        message_obj = await self.create_message(user_id, message)

        # Отправляем сообщение всем пользователям в чате
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_obj
            }
        )

    async def chat_message(self, event):
        """Отправка сообщения клиентам"""
        await self.send_json(event["message"])

    @sync_to_async
    def create_message(self, user_id, text):
        """Создание сообщения в базе данных"""
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(conversation=conversation, user_id=user_id, text=text)
        return MessageSerializer(message).data  # Сериализуем и отправляем
