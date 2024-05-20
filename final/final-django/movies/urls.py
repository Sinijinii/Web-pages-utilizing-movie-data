# urls.py 파일에서 해당 뷰를 등록합니다.
from django.urls import path
from .views import MovieSimilarityView
from . import views

urlpatterns = [
    # path('movies/', views.movie_list),
    path('movie-similarity/', MovieSimilarityView.as_view(), name='movie_similarity'),
]