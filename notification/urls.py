

from django.urls import path
from .views import SaveFCMToken

urlpatterns = [
    path("register-fcm-token/", SaveFCMToken.as_view()),
]
