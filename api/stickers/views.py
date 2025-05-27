from rest_framework import serializers, viewsets
from .models import Sticker


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = '__all__'


class StickerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing stickers.
    """
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer

    def perform_create(self, serializer):
        """
        Override the create method to handle any custom logic
        if required during Sticker creation.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Optional: Handle custom actions during updates.
        """
        serializer.save()