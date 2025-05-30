from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from .models import Album
from ..stickers.models import StickerGroup, Sticker

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


from api.stickers.views import StickerSerializer


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = ['user']


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def retrieve(self, request, *args, **kwargs):
        # Get the album by ID
        album = get_object_or_404(Album, pk=kwargs['pk'])

        album_data = self.get_serializer(album).data

        # Build the hierarchy data
        sticker_groups_data = []
        sticker_groups = StickerGroup.objects.filter()  # Assuming you link StickerGroup with Album

        for group in sticker_groups:
            stickers = Sticker.objects.filter(sticker_group=group, album=album).order_by(
                'id'
            )
            sticker_data = [
                model_to_dict(sticker) for sticker in stickers
            ]

            # Add group and its stickers
            sticker_groups_data.append({
                group.id: {
                    "stickers": sticker_data
                }
            })

        # Build the final response structure
        response_data = {
            "album": album_data,
            "sticker_groups": sticker_groups_data
        }

        return Response(response_data)


# Create your views here.
