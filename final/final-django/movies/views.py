from itertools import chain
from typing import Set, List, Dict, Any
from rest_framework.response import Response
from rest_framework import status
from movies.models import Movie
from accounts.models import UserInfo
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from movies.models import OTTPlatform, Movie
from accounts.models import UserInfo
from accounts.serializers import MovieSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse


@api_view(['GET'])
def movie_list(request):
    # 평점 높은 순, 평가 많은 순, 최신 개봉 순
    top_voted = Movie.objects.order_by('-vote_average')[:20]
    most_voted = Movie.objects.order_by('-vote_count')[:20]
    latest_movies = Movie.objects.order_by('-release_date')[:20]

    top = MovieSerializer(top_voted, many=True)
    most = MovieSerializer(most_voted, many=True)
    latest = MovieSerializer(latest_movies, many=True)

    data = {
      'top' : top.data,
      'most' : most.data,
      'latest': latest.data
    }
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loginmovie_list(request):
    userinfo = get_object_or_404(UserInfo, user=request.user)
    userott = userinfo.selectedotts.all()
    data = {}
    for a in userott:
      ott = get_object_or_404(OTTPlatform, pk = a.id)
      serializer = MovieSerializer(ott.movies.order_by('-vote_average')[:20], many=True)
      data[f"{a.name}"] = serializer.data
    
    return Response(data=data, status=status.HTTP_200_OK)

def calculate_similarity(set1: Set[str], set2: Set[str]) -> int:
    return len(set1 & set2)

def extract_combined_data(movies: List[Movie]) -> (Set[str], Set[str]):
    all_casts = set(chain.from_iterable(movie.casts for movie in movies))
    all_genres = set(chain.from_iterable(movie.genres.values_list('name', flat=True) for movie in movies))
    return all_casts, all_genres

def get_movie_data(movie: Movie) -> (Set[str], Set[str]):
    return set(movie.casts), set(movie.genres.values_list('name', flat=True))

def calculate_similarities(target_casts: Set[str], target_genres: Set[str], comparison_data: List[Movie]):
    similarity_casts = []
    similarity_genres = []
    
    for movie in comparison_data:
        movie_casts, movie_genres = get_movie_data(movie)
        cast_similarity = calculate_similarity(target_casts, movie_casts)
        genre_similarity = calculate_similarity(target_genres, movie_genres)
        similarity_casts.append((movie, cast_similarity))
        similarity_genres.append((movie, genre_similarity))
    
    top_10_casts = sorted(similarity_casts, key=lambda x: x[1], reverse=True)[:10]
    top_10_genres = sorted(similarity_genres, key=lambda x: x[1], reverse=True)[:10]
    
    return top_10_casts, top_10_genres



@api_view(['GET'])
def MovieSimilarityView(request):
    user = request.user
    user_info = user.userinfo
    selec_data = user_info.selectedmovies.all()
    selec2_data = Movie.objects.all()

    selec_casts, selec_genres = extract_combined_data(selec_data)
    top_10_casts_selec2, top_10_genres_selec2 = calculate_similarities(selec_casts, selec_genres, selec2_data)


    result = {
    "top_10_casts_selec2": [
        {
            "title": movie[0].title,
            "poster_path": movie[0].poster_path,
            "movie_id": movie[0].id,
            "casts": movie[0].casts,
            "genres": [genre.name for genre in movie[0].genres.all()],  # genres 필드 순회하여 각 객체의 name 속성을 추출
            "overview": movie[0].overview,
            "ott_platforms": [platform.name for platform in movie[0].ott_platforms.all()],  # ott_platforms 필드 순회하여 각 객체의 name 속성을 추출
        }
        for movie in top_10_casts_selec2
    ],
    "top_10_genres_selec2": [
        {
            "title": movie[0].title,
            "poster_path": movie[0].poster_path,
            "movie_id": movie[0].id,
            "casts": movie[0].casts,
            "genres": [genre.name for genre in movie[0].genres.all()],  # genres 필드 순회하여 각 객체의 name 속성을 추출
            "overview": movie[0].overview,
            "ott_platforms": [platform.name for platform in movie[0].ott_platforms.all()],  # ott_platforms 필드 순회하여 각 객체의 name 속성을 추출
        }
        for movie in top_10_genres_selec2
    ]}

    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def MovieDetail(request, movie_id):
    User = get_user_model()
    movie = Movie.objects.get(id=movie_id)
    likes = []
    for userinfo in movie.likes.all():
        user = get_object_or_404(User, id = userinfo.id)
        likes.append(user.username)
    data = {
    'title': movie.title,
    'poster_path': movie.poster_path,
    'genres': [genre.name for genre in movie.genres.all()],  # genres 필드 순회하여 각 객체의 name 속성을 추출
    'casts': movie.casts,
    'overview': movie.overview,
    'ott_platforms': [platform.name for platform in movie.ott_platforms.all()],  # ott_platforms 필드 순회하여 각 객체의 name 속성을 추출
    'vote_average': movie.vote_average,
    "likes": likes,
    }
    return JsonResponse(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    userinfo = get_object_or_404(UserInfo, user=request.user)
    # 이미 좋아요를 했으면 좋아요 취소

    if userinfo in movie.likes.all():
        movie.likes.remove(userinfo)
        liked = False
        userinfo.selectedmovies.remove(Movie.objects.get(id=movie_id))
    # 좋아요를 하지 않았으면 좋아요 누르기
    else:
        movie.likes.add(userinfo)
        liked = True
        userinfo.selectedmovies.add(Movie.objects.get(id=movie_id))
    
    return JsonResponse({'liked': liked, 'likes_count': movie.likes.count()})

def SearchMovie(request,movietitle):
    # 제목에 해당하는 영화를 검색
    movies = Movie.objects.filter(title__icontains=movietitle)
    
    # 검색 결과가 있을 경우
    if movies.exists():
        # 첫 번째 검색 결과를 선택
        movie = movies.first()
        # 검색 결과를 JSON 형식으로 반환
        data = {

            'id':movie.id,
            # 필요한 다른 필드들을 추가로 포함할 수 있음
        }
        return JsonResponse(data)
    else:
        # 검색 결과가 없을 경우
        return JsonResponse({'error': '영화를 찾을 수 없습니다.'}, status=404)
