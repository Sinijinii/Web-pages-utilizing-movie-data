import json
import requests

class MovieAPI:
    def __init__(self, api_key):
        self.base_url = 'https://api.themoviedb.org/3'
        self.params = {
            'api_key': api_key,
            'language': 'ko'
        }
        self.genre_dict = self.get_genres()

    # 장르 번호를 한글로 바꾸기 위한 함수
    def get_genres(self):
        genre_dict = {}
        genres_response = requests.get(f"{self.base_url}/genre/movie/list", params=self.params)
        if genres_response.status_code == 200:
            genres_data = genres_response.json()['genres']
            for genre_data in genres_data:
                genre_dict[genre_data['id']] = genre_data['name']
        else:
            print("장르 정보를 가져오는데 문제가 발생했습니다.")
        return genre_dict

    def get_movie_info(self, movie_id):
        movie_url = f"{self.base_url}/movie/{movie_id}"
        response = requests.get(movie_url, params=self.params)
        if response.status_code == 200:
            movie_info = response.json()
            # 제목, 아이디, 포스터 URL, 장르, 주연배우 5명 정보만 받아오기
            movie_data = {
                "title": movie_info['title'],
                "movie_id": int(movie_id),
                "poster_url": f"https://image.tmdb.org/t/p/w500/{movie_info['poster_path']}" if movie_info['poster_path'] else None,
                "genres": [self.genre_dict[genre['id']] for genre in movie_info.get('genres', [])],
                "actors": [actor['name'] for actor in requests.get(f"{self.base_url}/movie/{movie_id}/credits", params=self.params).json()['cast'][:5]]
            }
            return movie_data
        else:
            print(f"영화 정보를 가져오는데 문제가 발생했습니다. 응답 코드: {response.status_code}")
            return None

# 선택영화 20개를 가져오는 함수
def fetch_and_save_movies(api_key, movie_ids, output_file):
    movie_api = MovieAPI(api_key)
    movies_info = []
    for movie_id in movie_ids:
        movie_data = movie_api.get_movie_info(movie_id)
        if movie_data:
            movies_info.append(movie_data)
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(movies_info, json_file, ensure_ascii=False, indent=4)

# 우리가 고른 영화 20개 TMDB ID값
movie_ids = ['496243', '27205', '68721', '19995', '635302', '296096', '49797', '862', '122906','372058', '278', '313369', '361743', '423', '138843', '838209', '155', '634649', '157336', '158445']
fetch_and_save_movies('7c11fe750835c7c0b4c2bb32573c709f', movie_ids, 'select_movies.json')

# TMDB 내 API키 : 7c11fe750835c7c0b4c2bb32573c709f