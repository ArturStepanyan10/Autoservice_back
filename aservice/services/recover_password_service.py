import random

from django.core.cache import cache
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError

from aservice.html_messages.password_reset_message import get_password_reset_html_message
from aservice.models import User
from AutoService import settings


class RecoverPasswordService:
    def __init__(self, email: str, code: str | None = None, new_password: str | None = None):
        self.email = validate_email(email)
        self.code = code
        self.new_password = new_password

    def get_user(self) -> User:
        """
        Метод используется для получения пользователя.
        :raise ValidationError: Если пользователь с таким e-mail в системе не найден.
        :return: Возвращает объект модели User.
        """

        try:
            return User.objects.get(email=self.email)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            raise ValidationError("Пользователь с таким e-mail не найден.")

    def generate_random_code(self) -> str:
        """
        Генерирует 6-значный код и сохраняет его в временное хранлище Redis.
        """
        user = self.get_user()
        reset_code = str(random.randint(100000, 999999))
        cache_key = f"password_reset_code_{user.id}"
        cache_timeout = 60
        cache.set(cache_key, reset_code, timeout=cache_timeout)
        return reset_code

    def verify_reset_code(self) -> bool:
        """
        Проверяет, совпадает ли введённый код с кодом восстановления, сохранённым в кэше.
        :raise ValidationError: Если код не был прислан в систему.
        :return: Возвращает True, если совпадает код, иначе False.
        """

        if self.code is None:
            raise ValidationError("Код не был прислан")
        user = self.get_user()
        cache_key = f"password_reset_code_{user.id}"
        stored_code = cache.get(cache_key)
        if stored_code and stored_code == self.code:
            cache.delete(cache_key)
            return True
        return False

    def send_code_to_mail(self):
        """
        Отправляет письмо с кодом на почту пользователя.
        """
        reset_code = self.generate_random_code()
        html_message = get_password_reset_html_message(reset_code)
        send_mail(
            subject="[AutoMaster] Письмо для сброса пароля",
            message="Код восстановления",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            html_message=html_message,
        )

    def confirm_password(self):
        """
        Устанавливает новый пароль пользователю.
        :raises ValidationError:
            - Если код, прописанный пользователем был неверный или время его жизни в redis истекло.
            - Если новый пароль не отличается от старого.
        """

        user = self.get_user()
        if self.new_password == user.password:
            raise ValidationError("Новый код должен отличаться от старого.")
        if self.verify_reset_code():
            user.set_password(self.new_password)
            user.save()
        else:
            raise ValidationError("Неверный или истекший код.")
