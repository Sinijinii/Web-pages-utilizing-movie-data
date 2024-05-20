from rest_framework import serializers
from .models import UserInfo
from movies.models import OTTPlatform, Movie, Genre

class OttSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTTPlatform
        fields = ('id',)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id','poster_path','vote_average','vote_count','release_date')
        
class UserInfoSerializer(serializers.ModelSerializer):
    
    selectedmovies = MovieSerializer(required=False)
    selectedotts = OttSerializer(required=False)

    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ('user',)