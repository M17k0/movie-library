"""
Implements the integration with the tmdb API
"""
import dotenv
import os
import requests

from urllib.parse import quote
from typing import Optional

from .tmdb_models.movie_model import MovieModel, GenreModel

tmdb_base_url =  "https://api.themoviedb.org/3/"
tmdb_poster_url = "https://image.tmdb.org/t/p/w185/"

def get_api_key() -> Optional[str]:
    """
    Get the TMDB API key from the environment
    """
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("TMDB API key is not configured")
    
    return api_key

def get_tmdb_request_headers() -> dict:
    """
    Get common http headers for TMDB requests
    """
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    return headers

def search_movie(name, page=1) -> list[MovieModel]:
    """
    Get movies from TMDB by keywords
    """
    url = tmdb_base_url + f"search/movie?query={quote(name)}&page={page}"

    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    data = response.json()
    movies = [MovieModel(id=movie["id"],
                         title=movie["title"],
                         poster=tmdb_poster_url + movie["poster_path"],
                         release_date=movie["release_date"])
              for movie in data["results"]
              if movie["poster_path"] != None]

    return movies

def get_movie_by_id(movie_id: int) -> MovieModel:
    """
    Get movie from TMDB by TMDB id
    """
    url = tmdb_base_url + f"movie/{movie_id}"

    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    data = response.json()

    movie = MovieModel(id=data["id"],
                       title=data["title"],
                       poster=tmdb_poster_url + data["poster_path"],
                       release_date=data["release_date"])
    
    movie.genres = [GenreModel(id=genre["id"],
                               name=genre["name"])
                    for genre in data["genres"]]

    return movie

def get_tmdb_genres() -> list[GenreModel]:
    """
    Get all available genres for movies from TMDB
    """
    url = tmdb_base_url + "genre/movie/list"
    
    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    data = response.json()
    
    all_genres = [GenreModel(id=genre["id"],
                             name=genre["name"]) 
                  for genre in data["genres"]]
    
    return all_genres
    
def get_reccomendations(movie_id: int) -> list[MovieModel]:
    """
    Get similar movies for TMDB movie id
    """
    url = tmdb_base_url + f"movie/{movie_id}/recommendations"
    
    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    data = response.json()
    
    movies = [MovieModel(id=movie["id"],
                         title=movie["title"],
                         poster=tmdb_poster_url + movie["poster_path"],
                         release_date=movie["release_date"])
              for movie in data["results"] 
              if movie["poster_path"] != None]
    
    return movies

def get_movies_by_genre(genre: int) -> list[MovieModel]:
    """
    Get best rated moviesby genre from TMDB
    """
    url = tmdb_base_url + f"discover/movie?with_genres={genre}&sort_by=vote_average.desc&vote_count.gte=10000"
    
    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    data = response.json()
    
    movies = [MovieModel(id=movie["id"],
                         title=movie["title"],
                         poster=tmdb_poster_url + movie["poster_path"],
                         release_date=movie["release_date"])
              for movie in data["results"]
              if movie["poster_path"] != None]
    
    return movies