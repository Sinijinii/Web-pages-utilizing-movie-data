from django.urls import path
from . import views
from .views import MovieSimilarityView



urlpatterns = [
  path('movies/', views.movie_list),
  path('recommend/', views.MovieSimilarityView, name='Movie_similarity_view'),
  path('detail/<int:movie_id>/', views.MovieDetail, name='MovieDetail'),
  path('loginmovies/', views.loginmovie_list),
]