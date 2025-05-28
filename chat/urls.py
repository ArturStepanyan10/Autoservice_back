from django.urls import path, include
from rest_framework import routers

from chat.views import ConversationViewSet, MessageViewSet, ConversationCreateOrGetView

router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/', ConversationCreateOrGetView.as_view(), name='create_or_get_conversation'),

]
