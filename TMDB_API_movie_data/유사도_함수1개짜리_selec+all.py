import json
from collections import Counter
from itertools import chain

def main():
    # Step 1: 파일 읽기
    with open('selec.json', 'r', encoding='utf-8') as f:
        selec_data = json.load(f)

    with open('allmovie.json', 'r', encoding='utf-8') as f:
        allmovie_data = json.load(f)

    # Step 2: 데이터 전처리
    def extract_combined_data(movies):
        all_casts = set(chain.from_iterable(movie['casts'] for movie in movies))
        all_genres = set(chain.from_iterable(movie['genres'] for movie in movies))
        return all_casts, all_genres

    selec_casts, selec_genres = extract_combined_data(selec_data)

    def get_movie_data(movie):
        return set(movie['fields']['casts']), set(movie['fields']['genres'])

    # Step 3: 유사도 계산
    def calculate_similarity(set1, set2):
        return len(set1 & set2)

    similarity_casts = []
    similarity_genres = []

    for movie in allmovie_data:
        movie_casts, movie_genres = get_movie_data(movie)
        cast_similarity = calculate_similarity(selec_casts, movie_casts)
        genre_similarity = calculate_similarity(selec_genres, movie_genres)
        similarity_casts.append((movie, cast_similarity))
        similarity_genres.append((movie, genre_similarity))

    # 각 기준에 따라 상위 10개 영화 선택
    top_10_casts = sorted(similarity_casts, key=lambda x: x[1], reverse=True)[:10]
    top_10_genres = sorted(similarity_genres, key=lambda x: x[1], reverse=True)[:10]

    # Step 4: 결과 저장
    result = {
        "top_10_casts": [movie[0] for movie in top_10_casts],
        "top_10_genres": [movie[0] for movie in top_10_genres]
    }

    with open('usadowls.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print("usadowls.json 파일이 생성되었습니다.")

# 메인 함수 호출
if __name__ == "__main__":
    main()
