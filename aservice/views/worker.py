from rest_framework.generics import ListAPIView

from aservice.models import Appointment
from aservice.serializers import AppointmentSerializer


class AppointmentView(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

