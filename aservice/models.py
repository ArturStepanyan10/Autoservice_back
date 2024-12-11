from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    role = models.CharField(max_length=100, verbose_name='РОЛЬ')

    def __str__(self):
        return f"{self.last_name} {self.role}"


class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.PositiveIntegerField(null=True, verbose_name='Год')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Цвет')
    vin = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='VIN')
    license_plate = models.CharField(max_length=15, unique=True, blank=False, null=False, verbose_name='Номер')
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='users_car')

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(blank=True, null=True)
    worker = models.ManyToManyField('Worker', blank=False, related_name='workers_sr')

    def __str__(self):
        return f"{self.title}"


class Worker(models.Model):
    position = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='users_wr')

    def __str__(self):
        return f"{self.user.last_name} - {self.specialization}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'CONFIRMED', 'ПОДТВЕРЖДЕНА'
        IN_PROGRESS = 'IN_PROGRESS', 'В ПРОЦЕССЕ'
        COMPLETED = 'COMPLETED', 'ЗАВЕРШЕНА'

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='cars_ap')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_ap')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services_ap')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='workers_ap')

    def __str__(self):
        return f"{self.user.last_name} - {self.date}"


class AppointmentDetails(models.Model):
    description = models.TextField()
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='details')


class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_rv')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services_rv')

    def __str__(self):
        return f"{self.user.last_name} - {self.rating}"


    