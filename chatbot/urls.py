from django.urls import path

from .views import FAQSearchView

urlpatterns = [
    path('faq-search/', FAQSearchView.as_view(), name='faq-search'),
]
