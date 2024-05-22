from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserInfo, Movie, OTTPlatform

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saveinfo(request, user_pk):
    try:
        userinfo = UserInfo.objects.get(user_id=user_pk)

    except UserInfo.DoesNotExist:
        return Response({'error': 'UserInfo not found.'}, status=status.HTTP_404_NOT_FOUND)

    # userinfo.selectedmovies.clear()
    userinfo.selectedotts.clear()

    for mid in request.data['selectedmovies']:
        userinfo.selectedmovies.add(Movie.objects.get(pk=mid))

    for oid in request.data['selectedotts']:
        userinfo.selectedotts.add(OTTPlatform.objects.get(pk=oid))

    return Response({'save':"success"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    userinfo = UserInfo.objects.get(user_id=user.pk)
    movies = set()
    otts = set()
    movies.update(userinfo.selectedmovies.values_list('id', flat=True))
    otts.update(userinfo.selectedotts.values_list('id', flat=True))

    result = {
        "user": user.pk,
        "selectedmovies": list(movies),
        "selectedotts": list(otts)
    }

    return Response(result)
