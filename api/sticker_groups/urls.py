from django.urls import path
from .views import StickerGroupListCreateView, StickerGroupRetrieveUpdateDestroyView

urlpatterns = [
    path('', StickerGroupListCreateView.as_view(), name='sticker-group-list'),
    path('<int:pk>/', StickerGroupRetrieveUpdateDestroyView.as_view(), name='sticker-group-detail'),
]
