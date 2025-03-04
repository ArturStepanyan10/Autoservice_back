import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from aservice.models import Car, Appointment, Service, Reviews, User
from aservice.serializers.userSerializers import (CarSerializer, AppointmentSerializer, ServiceSerializer, ReviewsSerializer,
                                                  RecordTimesSerializer)


class GetInfoUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id

        user = get_object_or_404(User, id=user_id)

        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'role': user.role,
        })


class PutInfoUser(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)

        data = request.data

        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'last_name' in data:
            user.phone_number = data['phone_number']

        user.save()

        return Response({
            'id': user.id,
            'phone_number': user.phone_number,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=status.HTTP_200_OK)


class BaseCarAppointmentViewSet(ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarViewSet(BaseCarAppointmentViewSet):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Car.objects.filter(user_id=user.id)


class AppointmentViewSet(BaseCarAppointmentViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user_id=user.id)

    def validate_phone_number(self, value):
        if not re.match(r'^(\+7|8)\d{10}$', value):
            raise serializers.ValidationError(
                "Введите корректный номер телефона!"
            )
        return value


class TimeByDateView(APIView):

    def get(self, request):
        date = request.query_params.get('date')

        if not date:
            return JsonResponse({'Ошибка': 'Дата обязательна'}, status=status.HTTP_400_BAD_REQUEST)

        records_times = Appointment.objects.filter(date=date)

        if records_times.exists():
            serializer = RecordTimesSerializer(records_times, many=True)
            return Response(serializer.data)
        else:
            return Response([])


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'pk'


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id', None)
        if service_id:
            return Reviews.objects.filter(service__pk=service_id)
        return Reviews.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]








