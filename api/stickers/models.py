from django.db import models

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

    def __str__(self):
        return f"{self.name} - {self.country} ({self.type})"

