from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MensagemViewSet

# Cria um roteador para registrar ViewSets automaticamente.
router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'mensagens', MensagemViewSet, basename='mensagem')

urlpatterns = [
    path('', include(router.urls)),
    path('conversas/<int:pk>/mensagens/', ChatViewSet.as_view({'get': 'listar_mensagens'}), name='chat-conversas-mensagens'),
]