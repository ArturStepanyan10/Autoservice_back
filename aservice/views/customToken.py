from rest_framework_simplejwt.views import TokenObtainPairView

from aservice.serializers.customTokenSerializers import CustomTokenObtainSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
