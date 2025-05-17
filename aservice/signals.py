import requests
from django.db.models.signals import pre_save
from django.dispatch import receiver

from aservice.models import Appointment
from notification.models import Device
from notification.utils import send_push_notification


@receiver(pre_save, sender=Appointment)
def send_status_change_notification(sender, instance, **kwargs):
    if not instance.pk:
        return

    old = Appointment.objects.get(pk=instance.pk)
    if old.status != instance.status:
        # Статус изменился
        user = instance.user
        devices = Device.objects.filter(user=user)
        for device in devices:
            send_push_notification(device.fcm_token, f"Статус вашей записи обновлён: {instance.status}")




