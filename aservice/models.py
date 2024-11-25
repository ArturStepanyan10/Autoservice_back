from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=255, blank=False, null=False)
    role = models.CharField(max_length=100)
    car = models.ForeignKey('Car', blank=True, null=True, on_delete=models.SET_NULL, related_name='cars')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField(null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    vin = models.CharField(max_length=50, unique=True, blank=False, null=False)
    license_plate = models.CharField(max_length=15, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.name}"


class Worker(models.Model):
    position = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        pass


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50)
    total_price = models.PositiveIntegerField()
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='cars')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='workers')


class AppointmentDetails(models.Model):
    description = models.TextField()
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='details')


class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.user.first_name} - {self.rating}"