from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from aservice.view import (
    AppointmentViewSet,
    CarViewSet,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ReviewViewSet,
    ServiceViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("service", ServiceViewSet, basename="service")
router.register(r"car", CarViewSet, basename="car")
router.register(r"appointment", AppointmentViewSet, basename="appointment")
router.register(r"review", ReviewViewSet, basename="review")

urlpatterns = router.urls
urlpatterns += [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
urlpatterns = [
    path(
        "password-reset-request/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
