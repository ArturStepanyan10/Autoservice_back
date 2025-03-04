from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from AutoService import settings
from aservice.models import User
from aservice.serializers.userSerializers import (UserSerializer, WorkerSerializer)

from aservice.utils import generate_random_code, verify_reset_code


class BaseRegistrationView(APIView):
    serializer_class = None

    def post(self, request):
        if not self.serializer_class:
            return Response('Serializer not defined')

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterUserView(BaseRegistrationView):
    serializer_class = UserSerializer


class RegisterWorkerView(BaseRegistrationView):
    serializer_class = WorkerSerializer


class PasswordResetRequestView(APIView):

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = generate_random_code(user)

            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; text-align: justify;">
                    <p>Здравствуйте!</p>

                    <p>Чтобы сбросить пароль от аккаунта на AutoMaster Autoservice, пропишите код в приложении, 
                    который ниже указан.</p>

                    <p style="font-size: 15px; color: blue; text-decoration: underline;">
                        {reset_code}
                    </p>

                    <p>Если вы не запрашивали изменение пароля, пожалуйста, проигнорируйте это сообщение.</p>
                     
                    <p>Команда Autoservice AutoMaster!</p>
                </body>
            </html>
            """
            send_mail(
                subject="[AutoMaster] Письмо для сброса пароля",
                message=f"Код восстановления",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message
            )

            return Response({"message": "Код восстановления отправлен."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            if verify_reset_code(user, code):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Пароль успешно изменён."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Неверный или истёкший код."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)
