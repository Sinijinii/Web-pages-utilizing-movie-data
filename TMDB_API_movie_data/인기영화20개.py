import json
import requests

# requests.get(이 안에는 url이 들어가야 한다)
Base_Url = 'https://api.themoviedb.org/3'
path = '/movie/popular'
# 쿼리스트링을 입력 할 때 params를 이용한다.
params = {
    'api_key': '7c11fe750835c7c0b4c2bb32573c709f',  # required
    'region': 'KR',        # optional
    'language': 'ko'    # optional
}

response = requests.get(Base_Url+path, params=params)

# 장르 정보를 담을 딕셔너리 생성
genre_dict = {}

# 만약 요청이 성공했다면
if response.status_code == 200:
    # JSON 응답에서 결과 추출
    results = response.json()['results']
    
    # 장르 정보 가져오기
    genres_response = requests.get(f"{Base_Url}/genre/movie/list", params=params)
    if genres_response.status_code == 200:
        genres_data = genres_response.json()['genres']
        for genre_data in genres_data:
            genre_dict[genre_data['id']] = genre_data['name']
    else:
        print("장르 정보를 가져오는데 문제가 발생했습니다.")
    
    # 결과를 확인하면서 출력
    best_movies = []
    for movie in results:
        # 포스터 이미지 가져오기
        poster_path = movie['poster_path']
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
        
        # 주연배우 목록 가져오기
        credits_url = f"{Base_Url}/movie/{movie['id']}/credits"
        credits_response = requests.get(credits_url, params=params)
        if credits_response.status_code == 200:
            cast = credits_response.json()['cast']
            actors = [actor['name'] for actor in cast[:5]]  # 최대 5명까지만 출력
        else:
            actors = None
        
        # 영화 정보를 딕셔너리로 저장
        movie_data = {
            "title": movie['title'],
            "movie_id": movie['id'],  # 영화 ID 저장
            "poster_url": poster_url,
            "genres": [genre_dict.get(genre_id, "알 수 없는 장르") for genre_id in movie['genre_ids']],  # 장르명으로 변환
            "actors": actors
        }
        best_movies.append(movie_data)
    
    # 영화 정보를 JSON 파일에 저장
    with open("best_movies.json", "w", encoding="utf-8") as json_file:
        json.dump(best_movies, json_file, ensure_ascii=False, indent=4)
else:
    print("영화 정보를 가져오는데 문제가 발생했습니다. 응답 코드:", response.status_code)
