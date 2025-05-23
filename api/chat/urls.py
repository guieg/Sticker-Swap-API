from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MensagemViewSet

# Cria um roteador para registrar ViewSets automaticamente.
router = DefaultRouter()
router.register(r'conversas', ChatViewSet)
router.register(r'mensagens', MensagemViewSet)

urlpatterns = [
    # Inclui as URLs geradas pelo roteador.
    path('', include(router.urls)),
]
