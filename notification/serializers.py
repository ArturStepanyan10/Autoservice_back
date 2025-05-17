from rest_framework import serializers

from notification.models import Device


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['fcm_token']
