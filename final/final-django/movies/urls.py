from django.urls import path
from . import views


urlpatterns = [
  path('movies/', views.movie_list),
  path('loginmovies/', views.loginmovie_list),
]