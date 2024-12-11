from rest_framework.response import Response
from rest_framework.views import APIView
from aservice.serializers import UserSerializer, WorkerSerializer
from aservice.utils import get_user_from_token


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


class InfoUserView(APIView):
    def get(self, request):
        user = get_user_from_token(request)
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