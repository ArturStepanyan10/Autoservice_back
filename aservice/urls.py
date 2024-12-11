from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from aservice.views.auth import RegisterUserView, RegisterWorkerView, InfoUserView, LogoutView
from aservice.views.user import CarViewSet, AppointmentViewSet, ServiceListView, ReviewViewSet

router = SimpleRouter()
router.register(r'carslist', CarViewSet)
router.register(r'appointadd', AppointmentViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/user/register/', RegisterUserView.as_view()),
    path('auth/worker/register/', RegisterWorkerView.as_view()),
    path('infoUser/', InfoUserView.as_view()),
    path('servicelist/', ServiceListView.as_view()),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]