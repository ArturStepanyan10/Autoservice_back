from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from aservice.views.auth import RegisterUserView, RegisterWorkerView, PasswordResetRequestView, PasswordResetConfirmView
from aservice.views.user import CarViewSet, AppointmentViewSet, ServiceListView, ReviewViewSet, \
    GetInfoUser, ServiceDetailView, TimeByDateView, PutInfoUser
from aservice.views.worker import AppointmentsByDateWorkerView

router = SimpleRouter()
router.register(r'carslist', CarViewSet, basename='car')
router.register(r'appointmentlist', AppointmentViewSet, basename='appointment')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/user/register/', RegisterUserView.as_view()),
    path('auth/worker/register/', RegisterWorkerView.as_view()),

    path('servicelist/', ServiceListView.as_view()),
    path('service/<int:pk>/', ServiceDetailView.as_view()),
    path('info/', GetInfoUser.as_view()),
    path('put/user/', PutInfoUser.as_view()),
    path('records/time/', TimeByDateView.as_view()),
    path('appointment/by/worker-date/', AppointmentsByDateWorkerView.as_view()),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("password-reset-request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

]


