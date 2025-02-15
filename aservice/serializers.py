from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import serializers
from aservice.models import User, Worker, Car, Appointment, Service, Reviews, Message, Dialog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password','first_name',
                  'last_name', 'role', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
        }

    def create(self, validated_data):
        if 'role' not in validated_data:
            validated_data['role'] = 'ROLE_CLIENT'

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'position', 'experience', 'specialization', 'user']

    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'ROLE_WORKER'
        user = UserSerializer().create(user_data)

        worker = Worker.objects.create(user=user, **validated_data)
        return worker


class CarSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['total_price', 'status']

    def validate_time(self, time):
        if time is None:
            raise serializers.ValidationError("Поле 'Время' обязательно для заполнения.")

        if time.hour < 9 or (time.hour == 19 and time.minute > 0) or time.hour > 19:
            raise serializers.ValidationError("Записаться нельзя! Автосервис работает с 9:00 до 19:00.")

        return time

    def validate_car(self, car):
        if car.user != self.context['request'].user:
            raise serializers.ValidationError("У вас нет такого автомобиля")
        return car

    def validate(self, attrs):
        worker = attrs.get('worker', None)
        date = attrs.get('date', None)
        time = attrs.get('time', None)

        if Appointment.objects.filter(worker=worker, date=date, time=time).exists():
            raise serializers.ValidationError(
                "На это время и дату мастер уже занят. Пожалуйста, выберите другое время.")

        return attrs

    def create(self, validated_data):
        service = validated_data['service']
        total_price = service.price

        appointment = Appointment.objects.create(total_price=total_price, **validated_data)

        return appointment


class RecordTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['time']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'is_published']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, attrs):
        service = attrs.get('service', None)

        if not Appointment.objects.filter(service=service, user=attrs.get('user'), status='ЗАВЕРШЕНА').exists():
            raise serializers.ValidationError("Вы не можете оставить отзыв, так как нет записей на эту услугу.")

        return attrs


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'dialog', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'dialog', 'sender', 'is_read']


class DialogSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = ['id', 'participants', 'messages']
        read_only_fields = ['id', 'messages']
