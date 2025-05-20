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
    number = models.PositiveIntegerField(editable=False)  # Positive integer, auto-incremented
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(default=0)  # Default to 0 for unsigned integers

    def save(self, *args, **kwargs):
        """Override the save method to ensure the `number` auto-increments."""
        if not self.id:  # For a new Sticker object
            # Get the last number for this album, or start at 1 if none exist
            last_sticker = Sticker.objects.filter(album=self.album).order_by('number').last()
            self.number = last_sticker.number + 1 if last_sticker else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.country} ({self.type})"