
from django.db import models

from api.accounts.models import User

class Album(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='album')


