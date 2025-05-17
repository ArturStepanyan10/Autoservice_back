from django.db.models.signals import post_save

from chat.models import Message
from django.dispatch import receiver
from notification.utils import send_push_notification


@receiver(post_save, sender=Message)
def message_created_handler(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        sender_user = instance.user

        if conversation.sender == sender_user:
            receiver_user = conversation.receiver
        else:
            receiver_user = conversation.sender

        # Отправляем пуш-уведомление
        send_push_notification(
            user=receiver_user,
            title=f"Новое сообщение от {sender_user.first_name}",
            body=instance.text
        )
