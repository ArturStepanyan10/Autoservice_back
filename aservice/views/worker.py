from datetime import datetime

from rest_framework.generics import ListAPIView

from aservice.models import Appointment
from aservice.serializers.workerSerializers import TodayRecordsSerializer


class AppointmentsByDateWorkerView(ListAPIView):
    serializer_class = TodayRecordsSerializer

    def get_queryset(self):
        user_pk = self.request.user.pk
        today = datetime.today().date()
        return Appointment.objects.filter(worker=user_pk, date=today)






