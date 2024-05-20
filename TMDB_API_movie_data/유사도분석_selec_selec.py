import json
from itertools import chain
from typing import Set, List, Dict, Any

# 유사도 계산 함수
def calculate_similarity(set1: Set[str], set2: Set[str]) -> int:
    return len(set1 & set2)

# 파일 읽기 함수
def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 데이터 전처리 함수
def extract_combined_data(movies: List[Dict[str, Any]]) -> (Set[str], Set[str]):
    all_casts = set(chain.from_iterable(movie['casts'] for movie in movies))
    all_genres = set(chain.from_iterable(movie['genres'] for movie in movies))
    return all_casts, all_genres

# 영화 데이터 추출 함수
def get_movie_data(movie: Dict[str, Any]) -> (Set[str], Set[str]):
    return set(movie['casts']), set(movie['genres'])

# 주어진 파일 경로에서 데이터 로드
selec_data = read_json_file('selec.json')
selec2_data = read_json_file('selec2.json')

# selec.json 데이터에서 casts와 genres 추출
selec_casts, selec_genres = extract_combined_data(selec_data)

# 유사도 계산 및 영화 정렬 함수
def calculate_similarities(target_casts: Set[str], target_genres: Set[str], comparison_data: List[Dict[str, Any]]):
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

# selec.json과 selec2.json의 유사도 계산
top_10_casts_selec2, top_10_genres_selec2 = calculate_similarities(selec_casts, selec_genres, selec2_data)

# 결과 저장
result = {
    "top_10_casts_selec2": [movie[0] for movie in top_10_casts_selec2],
    "top_10_genres_selec2": [movie[0] for movie in top_10_genres_selec2]
}

with open('usadowls_selec2.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("usadowls_selec2.json 파일이 생성되었습니다.")
