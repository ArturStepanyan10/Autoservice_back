import jwt
from rest_framework.exceptions import AuthenticationFailed

from aservice.models import User


def get_user_from_token(request):
    token = request.COOKIES.get('token')

    if not token:
        raise AuthenticationFailed("Пользователь не авторизован!")

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Пользователь не авторизован!")

    return User.objects.get(pk=payload['id'])