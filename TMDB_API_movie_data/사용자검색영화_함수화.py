import json
import requests

class MovieInfoRetriever:
    def __init__(self, api_key):
        self.base_url = 'https://api.themoviedb.org/3'
        self.api_key = api_key
        self.params = {
            'api_key': self.api_key,
            'language': 'ko'
        }

    def get_movie_info(self, movie_title):
        # 영화 검색 API 호출
        search_url = f"{self.base_url}/search/movie"
        search_params = {
            **self.params,
            'query': movie_title
        }
        search_response = requests.get(search_url, params=search_params)
        if search_response.status_code == 200:
            search_results = search_response.json()['results']
            if not search_results:
                return None  # 검색 결과가 없으면 None 반환
            movie = search_results[0]  # 첫 번째 검색 결과만 사용
            # 필요한 정보 가져오기
            movie_id = movie['id']
            movie_info = {
                "title": movie['title'],
                "movie_id": movie_id,
                "poster_url": f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}" if movie['poster_path'] else None,
                "genres": self.get_movie_genres(movie_id),
                "actors": self.get_movie_cast(movie_id)
            }
            return movie_info
        else:
            print("영화 정보를 가져오는데 문제가 발생했습니다. 응답 코드:", search_response.status_code)
            return None

    def get_movie_genres(self, movie_id):
        # 영화 장르 정보 가져오기
        genre_url = f"{self.base_url}/movie/{movie_id}"
        response = requests.get(genre_url, params=self.params)
        if response.status_code == 200:
            return [genre['name'] for genre in response.json().get('genres', [])]
        else:
            print("영화 장르 정보를 가져오는데 문제가 발생했습니다.")
            return []

    def get_movie_cast(self, movie_id):
        # 영화 주연배우 정보 가져오기
        cast_url = f"{self.base_url}/movie/{movie_id}/credits"
        response = requests.get(cast_url, params=self.params)
        if response.status_code == 200:
            return [actor['name'] for actor in response.json().get('cast', [])[:5]]
        else:
            print("주연배우 정보를 가져오는데 문제가 발생했습니다.")
            return []

def search_and_save_movie_info(api_key, movie_title):
    movie_retriever = MovieInfoRetriever(api_key)
    movie_info = movie_retriever.get_movie_info(movie_title)
    if movie_info:
        file_name = f"{movie_title}.json"  # 파일명을 영화 이름으로 지정
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(movie_info, json_file, ensure_ascii=False, indent=4)
    else:
        print(f"'{movie_title}'에 대한 영화 정보를 찾을 수 없습니다.")

# 함수를 사용하여 영화 정보 검색 및 저장
# API 뒤에 영화 이름 검색하면 되는데, 이름 정확하게 검색 안하면 안뜸 ㅠㅠ
# 예를 들어 '존윅'이라고 하면 안뜨고 '존 윅'이라고 띄어쓰기까지 정확하게 해야 뜸
search_and_save_movie_info('7c11fe750835c7c0b4c2bb32573c709f', '존 윅')
