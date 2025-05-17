import random

from django.db import models

from api.albuns.models import Album


class Sticker(models.Model):
    PLAYER = 'player'
    SELECTION = 'selection'
    SHIELD = 'shield'

    TYPE_CHOICES = [
        (PLAYER, 'Player'),
        (SELECTION, 'Selection'),
        (SHIELD, 'Shield'),
    ]

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    number = models.IntegerField(default=random.randint(1, 1000))
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} - {self.country} ({self.type})"

