from django.db import models
from django.conf import settings

# Create your models here.
class Netflix(models.Model):
  casts = models.JSONField()
  genre_ids = models.JSONField()
  overview = models.TextField()
  popularity = models.FloatField()
  poster_path = models.CharField(max_length=100)
  release_date = models.DateField()
  title = models.CharField(max_length=100)
  vote_average = models.FloatField()
  vote_count = models.IntegerField()
  provider_id = models.JSONField()

  def __str__(self):
      return self.title

class Disney(models.Model):
  casts = models.JSONField()
  genre_ids = models.JSONField()
  overview = models.TextField()
  popularity = models.FloatField()
  poster_path = models.CharField(max_length=100)
  release_date = models.DateField()
  title = models.CharField(max_length=100)
  vote_average = models.FloatField()
  vote_count = models.IntegerField()
  provider_id = models.JSONField()

  def __str__(self):
      return self.title
  
class Watcha(models.Model):
  casts = models.JSONField()
  genre_ids = models.JSONField()
  overview = models.TextField()
  popularity = models.FloatField()
  poster_path = models.CharField(max_length=100)
  release_date = models.DateField()
  title = models.CharField(max_length=100)
  vote_average = models.FloatField()
  vote_count = models.IntegerField()
  provider_id = models.JSONField()

  def __str__(self):
      return self.title
  
  class Movie(models.Model):
    casts = models.JSONField()
    genre_ids = models.JSONField()
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=100)
    release_date = models.DateField()
    title = models.CharField(max_length=100)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    provider_id = models.JSONField()
    
    def __str__(self):
      return self.title