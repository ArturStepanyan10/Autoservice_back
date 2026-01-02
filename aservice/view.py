from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from aservice.models import Appointment, Car, Reviews, Service, User
from aservice.pagination import CustomPagination
from aservice.serializers import (
    AppointmentSerializer,
    CarSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ReviewsSerializer,
    ServiceSerializer,
    UserSerializer,
)
from aservice.services.appointment_service import AppointmentService
from aservice.services.recover_password_service import RecoverPasswordService


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    ViewSet для работы с пользователями.

    Используется для предоставления операций с пользователями.
    Доступ разрешён при авторизации.

    :param serializer_class: Сериализатор для частичного обновления и создания пользователя,
    а также получения детальной информации по пользователю.
    :param permission_classes: Доступ только при авторизации.

    :return: Детальная информация пользователя, частичное обновление данных пользователя либо создание пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()


class PasswordResetRequestView(APIView):
    """
    View для отправки кода на почту пользователю.

    :param service_class: Класс сервиса, в котором происходит вся основная логика отправки кода.
    :param serializer_class: Класс для сериализации входных данных.
    """

    service_class = RecoverPasswordService
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email", None)
        self.service_class(email).send_code_to_mail()
        return Response("Код восстановления отправлен.", status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    View для изменения пароля.

    :param service_class: Класс сервиса, в котором происходит вся основная логика изменения пароля.
    :param serializer_class: Класс для сериализации входных данных.
    """

    service_class = RecoverPasswordService
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        self.service_class(
            email=data.get("email"),
            code=data.get("code"),
            new_password=data.get("new_password"),
        ).confirm_password()
        return Response("Пароль успешно изменен.", status=status.HTTP_200_OK)


class CarViewSet(ModelViewSet):
    """
    ViewSet для работы с автомобилями клиентов.

    Используется для предоставления операций с автомобилями клиентов.
    Доступ разрешён при авторизации.

    :param serializer_class: Сериализатор для частичного обновления и добавления автомобиля,
    а также получения детальной информации по пользователю, получения списка автомобилей.
    :param permission_classes: Доступ только при авторизации.
    :param pagination_class: Класс пагинации для вывода списка автомобилей.

    :return: Детальная информация об автомобиле, частичное обновление данных автомобиля, добавление автомобиля,
    удаление автомобиля из списка или вывод списка автомобилей.
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ServiceViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    ViewSet для работы с услугами автосервиса.

    Используется для предоставления операций с услугами автосервиса.

    :param serializer_class: Сериализатор для получения детальной информации по услуге или получения списка услуг.
    :param pagination_class: Класс пагинации для вывода списка услуг автосервиса.
    :param search_fields: Поле(-я), по которому можно будет производить поиск.
    :param ordering: Поле, по которому происходит сортировка.

    :return: Детальная информация по услуге, список услуг автосервиса.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ["title"]
    ordering = ["id"]


class AppointmentViewSet(ModelViewSet):
    """
    ViewSet для работы с записями на обслуживание в автосервисе.

    Используется для предоставления операций с записями на обслуживание в автосервисе.

    :param serializer_class: Сериализатор для получения детальной информации по записи
     или получения списка записей, создание записи, обновления записи или удаления записи.
    :param pagination_class: Класс пагинации для вывода списка записей на обслуживание.
    :param search_fields: Поле, по которому можно будет производить поиск.
    :param ordering: Поле, по которому происходит сортировка.

    :return: Детальная информация по записям, список записей, созданная запись,
    обновленная запись или удаленная запись.
    """

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = CustomPagination
    search_fields = ["service__name"]
    ordering = ["id"]
    # filterset_fields = ["services", "car__brand"]  # из-за services скорее всего придется писать класс
    service_class = AppointmentService

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        appointment = self.service_class(
            date=data.get("date"),
            time=data.get("time"),
            car=data.get("car"),
            user=request.user or None,
            email=data.get("email"),
            brand=data.get("brand"),
            model=data.get("model"),
            phone_number=data.get("phone_number"),
            description=data.get("description"),
            license_plate=data.get("license_plate"),
            year=data.get("year"),
            total=data.get("total"),
            services=data.get("services"),
        ).create_appointment()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    ViewSet для работы с отзывами на услуги автосервиса.

    Используется для предоставления операций с отзывами на услуги автосервиса.

    :param serializer_class: Сериализатор для получения списка отзывов, обновление отзыва,
    создание отзыва или удаления отзыва.
    :param pagination_class: Класс пагинации для вывода списка отзывов на услугу.
    :param search_fields: Поле, по которому можно будет производить поиск.

    :return: Список отзывов, созданный отзыв, обновленный отзыв или удаленная запись.
    """

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    pagination_class = CustomPagination
    # search_fields = ["services_"]
    filterset_fields = ["rating", "user"]
