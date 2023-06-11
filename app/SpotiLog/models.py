from django.db import models
from BuscadorConciertos.models import Artist, Concierto

# Create your models here.

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    playlist_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
