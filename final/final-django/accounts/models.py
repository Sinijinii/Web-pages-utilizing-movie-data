from django.contrib.auth.models import AbstractUser
<<<<<<< HEAD
from django.db import models

class User(AbstractUser):
    favorite_movies = models.ManyToManyField('Movie', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    tmdb_id = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return self.title
=======
from movies.models import Movie


class User(AbstractUser):
    pass

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info')
    selectedmovies = models.ManyToManyField(Movie, related_name='user')

    # def str(self):
    #     return f"{self.user.username}'s info"
>>>>>>> 447b93795535d857ea08738c6aa4b25809ff3938
