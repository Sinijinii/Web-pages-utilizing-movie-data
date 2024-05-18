from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    

    def __str__(self):
        return f"{self.user.username}'s info"