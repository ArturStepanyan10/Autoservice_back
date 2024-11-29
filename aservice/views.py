import datetime, jwt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from aservice.models import User
from .serializers import UserSerializer, WorkerSerializer


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


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Пользователь не найден')

        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='token', value=token, httponly=True, secure=True)
        response.data = {
            'token': token,
        }

        return response


class InfoUserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed("Пользователь не авторизован!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Пользователь не авторизован!")

        user = User.objects.get(pk=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': "success"
        }

        return response


