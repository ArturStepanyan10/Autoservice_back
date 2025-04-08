from django.urls import path, include
from rest_framework import routers

from chat.views import ConversationViewSet, MessageViewSet

router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls))
]
