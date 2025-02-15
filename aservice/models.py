import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from rest_framework.exceptions import ValidationError


phone_number_validator = RegexValidator(
    regex=r'^(\+7|8)\d{10}$',
    message="Введите корректный номер телефона, начинающийся с +7 или 8, например: +79005895219 или 89005895218."
)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='E-mail', max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True,
                                    validators=[phone_number_validator],
                                    verbose_name='Номер телефона')
    role = models.CharField(max_length=100, verbose_name='РОЛЬ')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.role}"


class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.PositiveIntegerField(null=True, verbose_name='Год')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Цвет')
    vin = models.CharField(max_length=17, unique=True, blank=False, null=False, verbose_name='VIN')
    license_plate = models.CharField(max_length=15, unique=True, blank=False, null=False, verbose_name='Номер')
    photo = models.ImageField(upload_to='car_photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото машины')
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='users_car',
                             verbose_name='Владелец')

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость')
    worker = models.ManyToManyField('Worker', blank=False, related_name='workers_sr', verbose_name='Рабочий')

    def __str__(self):
        return f"{self.title}"


class Worker(models.Model):
    position = models.CharField(max_length=100, verbose_name='Должность')
    specialization = models.CharField(max_length=100, verbose_name='Специальность')
    experience = models.PositiveIntegerField(verbose_name='Стаж')
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='users_wr', verbose_name='Механик')

    def __str__(self):
        return f"{self.user.last_name} - {self.specialization}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'ПОДТВЕРЖДЕНА'
        IN_PROGRESS = 'В ПРОЦЕССЕ'
        COMPLETED = 'ЗАВЕРШЕНА'

    date = models.DateField(verbose_name='День')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED, verbose_name='Статус')
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Стоимость услуги')
    car = models.ForeignKey('Car', blank=True, null=True, on_delete=models.CASCADE, related_name='cars_ap', verbose_name='Машина')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_ap', verbose_name='Клиент')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services_ap', verbose_name='Услуга')
    worker = models.ForeignKey('Worker', blank=True, null=True, on_delete=models.CASCADE, related_name='workers_ap',
                               verbose_name='Рабочий')
    phone_number = models.CharField(
        null=True, blank=True,
        unique=True,
        max_length=12,
        validators=[phone_number_validator]
    )

    def clean(self):
        if self.date < datetime.date.today():
            raise ValidationError("День уже прошел!")

    def __str__(self):
        return f"{self.user.last_name} - {self.date}"


class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    content = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Статус')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_rv', verbose_name='Клиент')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services_rv', verbose_name='Услуга')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.last_name}"


class Dialog(models.Model):
    participants = models.ManyToManyField('User', related_name="dialogs")

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]
        return f"Диалог: {', '.join(usernames)}"


class Message(models.Model):
    dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name="dialogs")
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_ms')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp})"



