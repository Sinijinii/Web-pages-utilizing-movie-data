from django.contrib.auth.models import AbstractUser
from movies.models import Movie
from django.db import models

class User(AbstractUser):
    pass

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info')
    selectedmovies = models.ManyToManyField(Movie, related_name='user')

    # def str(self):
    #     return f"{self.user.username}'s info"

