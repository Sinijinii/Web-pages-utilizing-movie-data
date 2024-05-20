from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    favorite_movies = models.ManyToManyField('Movie', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    tmdb_id = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return self.title