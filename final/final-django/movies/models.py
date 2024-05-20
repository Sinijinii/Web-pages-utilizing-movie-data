from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

# 영화 모델
class Movie(models.Model):
    casts = models.JSONField()
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField()
    title = models.CharField(max_length=100)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    genres = models.ManyToManyField('Genre', related_name='movies')
    ott_platforms = models.ManyToManyField('OTTPlatform', related_name='movies')
    # users = models.ManyToManyField(User, related_name='movies')

    # def __str__(self):
    #     return self.title

# OTT 플랫폼 모델
class OTTPlatform(models.Model):
    name = models.CharField(max_length=255)
    platformId = models.IntegerField()
    logopath = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.name

# 장르 모델
class Genre(models.Model):
    name = models.CharField(max_length=255)
    genreId = models.IntegerField()

    # def __str__(self):
    #     return self.name