from django.shortcuts import render

import json
from itertools import chain
from typing import Set, List, Dict, Any
from django.http import JsonResponse
from django.views import View

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404


import json
from itertools import chain
from typing import Set, List, Dict, Any
from django.http import JsonResponse
from django.views import View

class MovieSimilarityView(View):
    def calculate_similarity(self, set1: Set[str], set2: Set[str]) -> int:
        return len(set1 & set2)

    def read_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_combined_data(self, movies: List[Dict[str, Any]]) -> (Set[str], Set[str]):
        all_casts = set(chain.from_iterable(movie['casts'] for movie in movies))
        all_genres = set(chain.from_iterable(movie['genres'] for movie in movies))
        return all_casts, all_genres

    def get_movie_data(self, movie: Dict[str, Any]) -> (Set[str], Set[str]):
        return set(movie['casts']), set(movie['genres'])

    def calculate_similarities(self, target_casts: Set[str], target_genres: Set[str], comparison_data: List[Dict[str, Any]]):
        similarity_casts = []
        similarity_genres = []
        
        for movie in comparison_data:
            movie_casts, movie_genres = self.get_movie_data(movie)
            cast_similarity = self.calculate_similarity(target_casts, movie_casts)
            genre_similarity = self.calculate_similarity(target_genres, movie_genres)
            similarity_casts.append((movie, cast_similarity))
            similarity_genres.append((movie, genre_similarity))
        
        top_10_casts = sorted(similarity_casts, key=lambda x: x[1], reverse=True)[:10]
        top_10_genres = sorted(similarity_genres, key=lambda x: x[1], reverse=True)[:10]
        
        return top_10_casts, top_10_genres

    def get(self, request):
        # 주어진 파일 경로에서 데이터 로드
        selec_data = self.read_json_file('selec.json')
        selec2_data = self.read_json_file('selec2.json')

        # selec.json 데이터에서 casts와 genres 추출
        selec_casts, selec_genres = self.extract_combined_data(selec_data)

        # selec.json과 selec2.json의 유사도 계산
        top_10_casts_selec2, top_10_genres_selec2 = self.calculate_similarities(selec_casts, selec_genres, selec2_data)

        # 결과 저장
        result = {
            "top_10_casts_selec2": [movie[0] for movie in top_10_casts_selec2],
            "top_10_genres_selec2": [movie[0] for movie in top_10_genres_selec2]
        }

        return JsonResponse(result)



