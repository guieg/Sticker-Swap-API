from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Sticker


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'name', 'country', 'type']

class StickerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer
from django.shortcuts import render

# Create your views here.
