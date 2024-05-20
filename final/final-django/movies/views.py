from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from movies.models import OTTPlatform, Movie, Genre
from accounts.models import UserInfo
from accounts.serializers import MovieSerializer
from django.contrib.auth import get_user_model

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