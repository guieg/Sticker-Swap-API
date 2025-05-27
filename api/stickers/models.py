import random
from django.db import models
from api.albuns.models import Album
from api.sticker_groups.models import StickerGroup


class Sticker(models.Model):
    PLAYER = 'player'
    SELECTION = 'selection'
    SHIELD = 'shield'

    TYPE_CHOICES = [
        (PLAYER, 'Player'),
        (SELECTION, 'Selection'),
        (SHIELD, 'Shield'),
    ]

    number = models.PositiveIntegerField(default=0)  # Positive integer, auto-incremented
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sticker_group = models.ForeignKey(StickerGroup, on_delete=models.CASCADE, default=1)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)
    amount = models.PositiveIntegerField(default=0)  # Default to 0 for unsigned integers


    def __str__(self):
        return f"{self.name} - {self.country} ({self.type})"