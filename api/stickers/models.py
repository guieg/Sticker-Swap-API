import random
from django.db import models
from api.albuns.models import Album
from api.sticker_groups.models import StickerGroup


class Sticker(models.Model):

    text = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=100, default="")
    sticker_group = models.ForeignKey(StickerGroup, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)


