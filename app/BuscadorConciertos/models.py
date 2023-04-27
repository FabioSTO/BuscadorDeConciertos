from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Concierto(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    place = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='concerts')

    def __str__(self):
        return self.name
    
