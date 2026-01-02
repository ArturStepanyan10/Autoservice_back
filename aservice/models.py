from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django_extensions.db.models import (
    TimeStampedModel,
)
from django_softdelete.models import (
    SoftDeleteModel,
)

phone_number_validator = RegexValidator(
    regex=r"^(\8)\d{10}$",
    message="Введите корректный номер телефона, начинающийся с 8.",
)


class User(AbstractUser, TimeStampedModel, SoftDeleteModel):
    username = None
    email = models.EmailField(verbose_name="E-mail", max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.last_name


class Car(models.Model):
    MKPP = 1
    AKPP = 2
    ROBOT = 3
    VARIATOR = 4

    TRANSMISSION_TYPE = ((MKPP, "МКПП"), (AKPP, "АКПП"), (ROBOT, "Робот"), (VARIATOR, "Вариатор"))

    FORWARD = 1  # ПЕРЕДНИЙ
    REAR = 2  # ЗАДНИЙ
    FULL = 3  # ПОЛНЫЙ

    DRIVE_TYPE = ((FORWARD, "Передний"), (REAR, "Задний"), (FULL, "Полный"))

    brand = models.CharField(max_length=255, validators=[MinLengthValidator(2)], verbose_name="Марка")
    model = models.CharField(max_length=255, validators=[MinLengthValidator(2)], verbose_name="Модель")
    transmission_type = models.PositiveIntegerField(
        choices=TRANSMISSION_TYPE, default=MKPP, verbose_name="Тип трансмисии"
    )
    mileage = models.FloatField(verbose_name="Пробег")
    drive_type = models.PositiveIntegerField(choices=DRIVE_TYPE, default=FORWARD, verbose_name="Тип привода")
    year = models.CharField(
        max_length=4,
        validators=[MinLengthValidator(4)],
        verbose_name="Год",
    )
    color = models.CharField(max_length=255, verbose_name="Цвет")
    vin = models.CharField(
        max_length=17,
        validators=[MinLengthValidator(17)],
        unique=True,
        verbose_name="ВИН",
    )
    license_plate = models.CharField(
        max_length=8, validators=[MinLengthValidator(8)], unique=True, verbose_name="Гос. номер"
    )
    photo = models.ImageField(
        upload_to="car_photos/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name="Фото автомобиля",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name="Владелец автомобиля",
    )

    def __str__(self):
        return self.brand, self.model


class Service(TimeStampedModel, SoftDeleteModel):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(3)], verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    total = models.PositiveIntegerField(verbose_name="Сумма")

    def __str__(self):
        return self.title


class Appointment(TimeStampedModel, SoftDeleteModel):
    class Status(models.TextChoices):
        CREATED = "CREATED", "СОЗДАНА"
        IN_PROGRESS = "IN_PROGRESS", "В ПРОЦЕССЕ"
        COMPLETED = "COMPLETED", "ЗАВЕРШЕНА"
        CANCELLED = "CANCELLED", "ОТМЕНЕНА"

    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    status = models.CharField(choices=Status.choices, default=Status.CREATED, verbose_name="Статус")
    car = models.ForeignKey(
        "Car",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Машина",
    )
    user = models.ForeignKey(
        "User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
    )
    services = models.ManyToManyField("Service", verbose_name="Услуги")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True, max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_number_validator, MinLengthValidator(11)],
        verbose_name="Номер телефона",
    )
    description = models.TextField(verbose_name="Описание проблемы", blank=True, null=True)
    brand = models.CharField(max_length=255, validators=[MinLengthValidator(2)], null=True, verbose_name="Марка")
    model = models.CharField(max_length=255, validators=[MinLengthValidator(2)], null=True, verbose_name="Модель")
    license_plate = models.CharField(
        max_length=8, validators=[MinLengthValidator(8)], unique=True, null=True, verbose_name="Гос. номер"
    )
    year = models.CharField(
        max_length=4,
        validators=[MinLengthValidator(4)],
        verbose_name="Год",
    )
    total = models.PositiveIntegerField(verbose_name="Окончательная сумма")


class Reviews(TimeStampedModel):
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг"
    )
    content = models.TextField(blank=True, null=True, verbose_name="Отзыв")
    is_published = models.BooleanField(default=True, verbose_name="Статус")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Клиент")
    services = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        verbose_name="Услуга",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.last_name
