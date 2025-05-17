from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Album
from ..stickers.models import Sticker
from rest_framework.serializers import ModelSerializer
from ..accounts.models import User

from api.stickers.views import StickerSerializer


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = ['user']


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
from django.shortcuts import render

# Create your views here.
