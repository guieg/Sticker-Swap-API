from rest_framework import serializers
from .models import StickerGroup
from rest_framework import generics


class StickerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StickerGroup
        fields = '__all__'
from django.shortcuts import render

# Create your views here.
class StickerGroupListCreateView(generics.ListCreateAPIView):
    """
    View to list all sticker groups or create a new one.
    """
    queryset = StickerGroup.objects.all()
    serializer_class = StickerGroupSerializer


class StickerGroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a sticker group by id.
    """
    queryset = StickerGroup.objects.all()
    serializer_class = StickerGroupSerializer
