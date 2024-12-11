from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from aservice.models import Car, Appointment, Service, Reviews
from aservice.serializers import CarSerializer, AppointmentSerializer, ServiceSerializer, ReviewsSerializer


class BaseCarAppointmentViewSet(ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarViewSet(BaseCarAppointmentViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(BaseCarAppointmentViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]