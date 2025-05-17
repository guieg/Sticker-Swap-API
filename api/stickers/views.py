from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Sticker


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'number', 'name', 'country', 'type', 'album_id']

class StickerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer


# Create your views here.
