import datetime

from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from aservice.html_messages.appointment_message import get_appointment_html_message
from aservice.models import Appointment, Car, User
from AutoService import settings


class AppointmentService:
    """
    Сервис для работы с записями.
    """

    def __init__(
        self,
        date: datetime.date,
        time: datetime.time,
        car: Car | None = None,
        user: User | None = None,
        email: str | None = None,
        brand: str | None = None,
        model: str | None = None,
        phone_number: str | None = None,
        description: str | None = None,
        license_plate: str | None = None,
        year: int | None = None,
        total: int | None = None,
        services: list[int] | None = None,
    ):
        self.date = date
        self.time = time
        self.car = car
        self.user = user
        self.email = email
        self.brand = brand
        self.model = model
        self.phone_number = phone_number
        self.description = description
        self.license_plate = license_plate
        self.year = year
        self.total = total
        self.services = services

        self._validate()

    def _validate(self):
        time_hour = self.time.hour
        today = datetime.date.today()
        if time_hour < 9 or time_hour > 19:
            raise ValidationError("Автосервис работает c 9:00 до 19:00.")
        if time_hour > 18:
            raise ValidationError("Последнюю запись можно сделать в 18:00. Автосервис работает до 19:00.")

        if self.date == today and datetime.datetime.now().hour >= time_hour:
            raise ValidationError("Нельзя записаться на прошедшее время.")
        if self.date < today or self.date > today + datetime.timedelta(days=14):
            raise ValidationError("Можно выбрать дату только в диапазоне от сегодня до 14 дней вперёд.")

    def create_appointment(self):
        base_data = {
            "date": self.date,
            "time": self.time,
            "status": Appointment.Status.CREATED,
            "services": self.services,
            "description": self.description,
            "phone_number": self.phone_number,
        }

        if self.user:
            base_data.update(
                {
                    "user": self.user,
                    "car": self.car,
                }
            )
        else:
            base_data.update(
                {
                    "email": self.email,
                    "brand": self.brand,
                    "model": self.model,
                    "license_plate": self.license_plate,
                    "year": self.year,
                }
            )

        appointment = Appointment.objects.create(**base_data)
        self.send_email()
        return appointment

    def send_email(self):
        html_message = get_appointment_html_message(self.date, self.time, self.services)

        if self.email:
            send_mail(
                subject="[AutoMaster] Информация о записи",
                message="Информация о записи",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.email],
                html_message=html_message,
                fail_silently=False,
            )
