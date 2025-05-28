from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from aservice.models import Appointment
from aservice.serializers.workerSerializers import TodayRecordsSerializer


class BaseAppointmentsByDateWorkerView(ListAPIView):
    serializer_class = TodayRecordsSerializer
    permission_classes = [IsAuthenticated, ]
    filter_type = None

    # def get_queryset(self):
    #     user_pk = self.request.user.pk
    #     worker_pk = get_user_model().objects.get(id=user_pk).users_wr.id
    #     today = datetime.today().date()
    #
    #     if self.filter_type == "past":
    #         return Appointment.objects.filter(worker=worker_pk, date__lt=today)
    #     elif self.filter_type == "future":
    #         return Appointment.objects.filter(worker=worker_pk, date__gt=today)
    #     else:
    #         return Appointment.objects.filter(worker=worker_pk, date=today)


class TodayAppointmentsView(BaseAppointmentsByDateWorkerView):
    filter_type = "today"


class PastAppointmentsView(BaseAppointmentsByDateWorkerView):
    filter_type = "past"


class FutureAppointmentsView(BaseAppointmentsByDateWorkerView):
    filter_type = "future"


