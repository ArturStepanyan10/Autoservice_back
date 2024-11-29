from django.urls import path

from aservice.views import RegisterUserView, RegisterWorkerView, LoginView, InfoUserView, LogoutView

urlpatterns = [
    path('auth/user/register/', RegisterUserView.as_view()),
    path('auth/worker/register/', RegisterWorkerView.as_view()),
    path('login/', LoginView.as_view()),
    path('infoUser/', InfoUserView.as_view()),
    path('logout/', LogoutView.as_view()),
]