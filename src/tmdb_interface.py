import dotenv
import os
import requests

from urllib.parse import quote
from typing import Optional

from tmdb_models.movie_model import MovieModel, GenreModel

tmdb_base_url =  "https://api.themoviedb.org/3/"
tmdd_poster_url = "https://image.tmdb.org/t/p/w185/"

def get_api_key() -> Optional[str]:
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        #TODO
        ...
    
    return api_key

def search_movie(name, page=1) -> list[MovieModel]:
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    url = tmdb_base_url + f"search/movie?query={quote(name)}&page={page}"

    response = requests.get(url, headers=headers)
    data = response.json()
    movies = [MovieModel(id=movie["id"],
                         title=movie["title"],
                         poster="https://image.tmdb.org/t/p/w185/" + movie["poster_path"],
                         relese_date=movie["release_date"])
              for movie in data["results"] 
              if movie["poster_path"] != None]

    return movies

def get_movie_by_id(moie_id: int):
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    url = tmdb_base_url + f"movie/{moie_id}"

    response = requests.get(url, headers=headers)
    data = response.json()

    movie = MovieModel(id=data["id"],
                       title=data["original_title"],
                       poster=tmdd_poster_url + data["poster_path"],
                       relese_date=data["release_date"])
    
    movie.genres = [GenreModel(id=genre["id"],
                               name=genre["name"])
                    for genre in data["genres"]]

    return movie