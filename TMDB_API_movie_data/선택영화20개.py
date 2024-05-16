import json
import requests

# requests.get(이 안에는 url이 들어가야 한다)
Base_Url = 'https://api.themoviedb.org/3'

# 가져올 영화들의 ID 리스트
movie_ids = ['496243', '27205', '68721', '19995', '635302', '296096', '49797', '862', '122906','372058', '278', '313369', '361743', '423', '138843', '838209', '155', '634649', '157336', '158445']

# 쿼리스트링을 입력 할 때 params를 이용한다.
params = {
    'api_key': '7c11fe750835c7c0b4c2bb32573c709f',  # required
    'language': 'ko'    # optional
}

# 장르 정보를 담을 딕셔너리 생성
genre_dict = {}

# 장르 정보 가져오기
genres_response = requests.get(f"{Base_Url}/genre/movie/list", params=params)
if genres_response.status_code == 200:
    genres_data = genres_response.json()['genres']
    for genre_data in genres_data:
        genre_dict[genre_data['id']] = genre_data['name']
else:
    print("장르 정보를 가져오는데 문제가 발생했습니다.")

# 각 영화의 정보를 담을 리스트 생성
movies_info = []

# 각 영화의 정보 가져오기
for movie_id in movie_ids:
    # 특정 영화의 정보를 가져오기
    movie_url = f"{Base_Url}/movie/{movie_id}"
    response = requests.get(movie_url, params=params)
    
    # 만약 요청이 성공했다면
    if response.status_code == 200:
        movie_info = response.json()
        movie_data = {
            "title": movie_info['title'],
            "movie_id": int(movie_id),
            "poster_url": f"https://image.tmdb.org/t/p/w500/{movie_info['poster_path']}" if movie_info['poster_path'] else None,
            "genres": [genre_dict[genre['id']] for genre in movie_info.get('genres', [])],
            "actors": [actor['name'] for actor in requests.get(f"{Base_Url}/movie/{movie_id}/credits", params=params).json()['cast'][:5]]
        }
        movies_info.append(movie_data)
    else:
        print(f"영화 정보를 가져오는데 문제가 발생했습니다. 응답 코드: {response.status_code}")

# 영화 정보를 JSON 파일에 저장
with open("select_movies.json", "w", encoding="utf-8") as json_file:
    json.dump(movies_info, json_file, ensure_ascii=False, indent=4)
