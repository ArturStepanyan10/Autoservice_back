from firebase_admin import messaging
from notification.models import Device


def send_push_notification(user, title, body):
    # Получаем токены устройств пользователя
    tokens = list(Device.objects.filter(user=user).values_list('fcm_token', flat=True))

    if not tokens:
        return

    # Создаём сообщение
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
    )

    # Отправка
    response = messaging.send_multicast(message)

    print(f"Успешно отправлено: {response.success_count}, Ошибки: {response.failure_count}")

