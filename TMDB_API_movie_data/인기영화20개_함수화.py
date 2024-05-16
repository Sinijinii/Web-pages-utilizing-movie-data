import json
import requests

def get_best_movies(api_key):
    Base_Url = 'https://api.themoviedb.org/3'
    path = '/movie/popular'
    params = {
        'api_key': api_key,
        'region': 'KR',
        'language': 'ko'
    }

    response = requests.get(Base_Url + path, params=params)

    genre_dict = {}

    if response.status_code == 200:
        results = response.json()['results']

        genres_response = requests.get(f"{Base_Url}/genre/movie/list", params=params)
        if genres_response.status_code == 200:
            genres_data = genres_response.json()['genres']
            for genre_data in genres_data:
                genre_dict[genre_data['id']] = genre_data['name']
        else:
            print("장르 정보를 가져오는데 문제가 발생했습니다.")

        best_movies = []
        for movie in results:
            poster_path = movie['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None

            credits_url = f"{Base_Url}/movie/{movie['id']}/credits"
            credits_response = requests.get(credits_url, params=params)
            if credits_response.status_code == 200:
                cast = credits_response.json()['cast']
                actors = [actor['name'] for actor in cast[:5]]
            else:
                actors = None

            movie_data = {
                "title": movie['title'],
                "movie_id": movie['id'],
                "poster_url": poster_url,
                "genres": [genre_dict.get(genre_id, "알 수 없는 장르") for genre_id in movie['genre_ids']],
                "actors": actors
            }
            best_movies.append(movie_data)

        with open("best_movies.json", "w", encoding="utf-8") as json_file:
            json.dump(best_movies, json_file, ensure_ascii=False, indent=4)
    else:
        print("영화 정보를 가져오는데 문제가 발생했습니다. 응답 코드:", response.status_code)

# 함수 실행
get_best_movies('7c11fe750835c7c0b4c2bb32573c709f')
