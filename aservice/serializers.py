from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

from aservice.models import Appointment, Car, Reviews, Service, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email])


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email])
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, validators=[validate_password]
    )
    code = serializers.CharField(write_only=True)


class CarSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    services = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_services(self, obj: Appointment):
        return [(service.id, service.title) for service in obj.services.all()]

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        if view and getattr(view, "action", None) in ("list", "retrieve"):
            allowed_fields = ["id", "created", "services", "description", "car", "total"]
            return {field: fields[field] for field in allowed_fields}
        elif view and getattr(view, "action", None) == "partial_update":
            allowed_fields = ["date", "time", "description", "phone_number", "car"]
            return {field: fields[field] for field in allowed_fields}
        return fields


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = ["is_published"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        services = attrs.get("services")

        if not Appointment.objects.filter(services=services, user=user, status=Appointment.Status.COMPLETED).exists():
            raise serializers.ValidationError(
                "Вы не можете оставить отзыв, так как нет завершённых записей на эту услугу."
            )

        attrs["user"] = user
        return attrs
