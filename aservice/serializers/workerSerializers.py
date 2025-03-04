from rest_framework import serializers

from aservice.models import Appointment


class TodayRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['user', 'service', 'time']

