import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from rest_framework import serializers

from AutoService import settings
from aservice.models import User, Worker, Car, Appointment, Service, Reviews


NORMAL_HOUR_COST = 1000

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'role']
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
    status = serializers.CharField(source='get_status_display', read_only=True)
    worker = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status']

    def get_worker(self, obj):
        if obj.worker:
            return obj.worker.user.id, obj.worker.user.first_name, obj.worker.user.last_name
        return None

    def get_service(self, obj):
        return [(service.title, service.id) for service in obj.service.all()]

    def validate(self, data):
        date = data.get('date')
        time = data.get('time')
        if time is None:
            raise serializers.ValidationError({"time": "Поле 'Время' обязательно."})
        if time.hour < 9 or (time.hour == 19 and time.minute > 0) or time.hour > 19:
            raise serializers.ValidationError({"time": "Автосервис работает 9–19."})
        if date == datetime.date.today() and datetime.datetime.now().hour >= time.hour:
            raise serializers.ValidationError({"time": "Нельзя записаться в прошедшее время."})
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if instance.status == Appointment.Status.COMPLETED:
            total_labor = 0

            for service in instance.service.all():
                total_labor += float(service.labor_time) * float(service.difficulty_factor)

            if instance.loyalty_factor:
                total_labor_adjusted = total_labor * float(instance.loyalty_factor)

            instance.total_labor_time = round(total_labor, 2)
            instance.total_price = round(total_labor_adjusted * NORMAL_HOUR_COST, 2)

            instance.save()

        return instance


    def create(self, validated_data):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        user = getattr(request, 'user', None)

        if user and not isinstance(user, AnonymousUser):
            validated_data['user'] = user

        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; text-align: justify;">
                <h2>Здравствуйте!</h2>
                <p style="font-size: 16px; color: #555555;">
                    Вы успешно записались в автосервис <strong>AutoMaster</strong>.
                </p>
                <p style="font-size: 16px; color: #555555;">
                    <p style="font-size: 16px; color: #555555;">
                        Дублируем информацию записи:
                    </p>
                    <strong>Дата:</strong> {validated_data.get('date')}<br>
                    <strong>Время:</strong> {validated_data.get('time')}<br>
                    <strong>Услуга:</strong> {validated_data.get('service')}
                </p>
                <p style="font-size: 14px; color: #999999; margin-top: 30px;">
                    Если вы не записывались, просто проигнорируйте это сообщение.
                </p>
            </body>
        </html>
        """

        email = validated_data.get('email')
        if email:
            send_mail(
                subject="[AutoMaster] Письмо для сброса пароля",
                message=f"Код восстановления",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )

        return super().create(validated_data)


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

