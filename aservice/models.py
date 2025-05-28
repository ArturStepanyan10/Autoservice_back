import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, MinLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError


phone_number_validator = RegexValidator(
    regex=r'^(\+7|8)\d{10}$',
    message="Введите корректный номер телефона, начинающийся с +7 или 8, например: +79005895219 или 89005895218."
)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='E-mail', max_length=255, unique=True)
    role = models.CharField(max_length=32, verbose_name='РОЛЬ')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.role}"


class Car(models.Model):
    brand = models.CharField(max_length=128, validators=[MinLengthValidator(2)], verbose_name='Марка')
    model = models.CharField(max_length=128, validators=[MinLengthValidator(2)], verbose_name='Модель')
    year = models.CharField(max_length=4, validators=[MinLengthValidator(4)], null=True, blank=True, verbose_name='Год')
    color = models.CharField(max_length=64, blank=True, null=True, verbose_name='Цвет')
    vin = models.CharField(max_length=17, validators=[MinLengthValidator(17)], unique=True, blank=False, null=False,
                           verbose_name='ВИН')
    license_plate = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name='Гос. номер')
    photo = models.ImageField(upload_to='car_photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото машины')
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='users_car',
                             verbose_name='Владелец')

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"


class Service(models.Model):
    title = models.CharField(max_length=128, validators=[MinLengthValidator(5)], verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    # labor_time = models.DecimalField(max_digits=5, decimal_places=2)
    # difficulty_factor = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)

    def __str__(self):
        return f"{self.title}"


class Worker(models.Model):
    position = models.ForeignKey('Post', null=True, on_delete=models.SET_NULL, related_name='post',
                                 verbose_name='Должность')
    specialization = models.ForeignKey('Specialization', null=True, on_delete=models.SET_NULL, related_name='spec',
                                       verbose_name='Специальность')
    experience = models.PositiveIntegerField(verbose_name='Стаж')
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='users_wr', verbose_name='Механик')
    photo = models.ImageField(upload_to='workers_photos/', blank=True, null=True, verbose_name='Фото механика')

    def __str__(self):
        return f"{self.user.pk}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'CONFIRMED', 'ПОДТВЕРЖДЕНА'
        IN_PROGRESS = 'IN_PROGRESS', 'В ПРОЦЕССЕ'
        COMPLETED = 'COMPLETED', 'ЗАВЕРШЕНА'
        CANCELLED = 'CANCELLED', 'ОТМЕНЕНА'

    date = models.DateField(verbose_name='День')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(choices=Status.choices, default=Status.CONFIRMED, verbose_name='Статус')
    car = models.ForeignKey('Car', blank=True, null=True, on_delete=models.CASCADE, related_name='cars_ap',
                            verbose_name='Машина')
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='users_ap',
                             verbose_name='Клиент')
    service = models.ManyToManyField('Service', related_name='appointments', verbose_name='Услуги')
    worker = models.ForeignKey('Worker', blank=True, null=True, on_delete=models.CASCADE, related_name='workers_ap',
                               verbose_name='Рабочий')
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True, max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True,
                                    validators=[phone_number_validator, MinLengthValidator(11)],
                                    verbose_name='Номер телефона')
    description = models.TextField(verbose_name='Описание проблемы', blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True, validators=[MinLengthValidator(2)],
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=128, blank=True, null=True, validators=[MinLengthValidator(2)],
                                 verbose_name='Фамилия')
    # loyalty_factor = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    # total_labor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean(self):
        if self.date < datetime.date.today():
            raise ValidationError("День уже прошел!")


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


class Specialization(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(4)], verbose_name='Название')

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(4)], verbose_name='Название')

    def __str__(self):
        return self.title




