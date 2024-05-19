from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, OTTPlatform
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
    pass
    
class UserInfo(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info')
    selectedMovies = models.ManyToManyField(Movie, related_name='user')
    selectedOtts = models.ManyToManyField(OTTPlatform, related_name='user')