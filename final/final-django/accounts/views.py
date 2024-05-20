from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import UserInfoSerializer
from .models import UserInfo

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def saveinfo(request, user_pk):
    if request.method == 'POST':
        serializer = UserInfoSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=user_pk)
            return Response(serializer.data, status=status.HTTP_200_OK)