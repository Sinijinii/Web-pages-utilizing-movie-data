from rest_framework import serializers
from .models import UserInfo
from movies.models import OTTPlatform, Movie, Genre

# class OttSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTTPlatform
#         fields= '__all_-'

# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = '__all__'

# class UserInfoSerializer(serializers.ModelSerializer):
#     otts = OttSerializer(many=True, required=False)
#     genres = GenreSerializer(many=True, required=False)
#     class Meta:
#         model = UserInfo
#         fields = '__all__'
#         read_only_fields = ('user',)


class OttSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTTPlatform
        fields = ('id',)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id',)

# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = '__all__'
        
class UserInfoSerializer(serializers.ModelSerializer):
    # selectedmovies = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=True, required=False)
    # selectedotts = serializers.PrimaryKeyRelatedField(queryset=OTTPlatform.objects.all(), many=True, required=False)
    # selectedgenres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)
    
    selectedmovies = MovieSerializer(required=False)
    selectedotts = OttSerializer(required=False)

    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ('user',)