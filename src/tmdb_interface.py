"""
Implements the integration with the TMDB API

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

def fetch_tmdb_data(endpoint: str) -> dict:
    """
    Fetch data from TMDB endpoint and
    return a dictionary representing the TMDB response.
    """    
    url = tmdb_base_url + endpoint
    
    response = requests.get(url, headers=get_tmdb_request_headers())
    if response.status_code >= 300:
        raise ValueError(f"Bad response - status code: {response.status_code}")
    
    return response.json()

def create_movie_models(movies_data: list[dict]) -> list[MovieModel]:
    """
    Create MovieModel instances without genres from a list of dict of TMDB movies data("results")
    Used to visualize the movies for search/recommend/discover requests
    may also use the genres and just call create_full_movie_model()
    """
    return [MovieModel(id=movie["id"],
                       title=movie["title"],
                       poster=tmdb_poster_url + movie["poster_path"],
                       release_date=movie["release_date"])
            for movie in movies_data
            if movie["poster_path"] is not None]

def create_full_movie_model(movie_data: dict) -> MovieModel:
    """
    Create full MovieModel from a dict of TMDB data for a single movie
    """
    movie = MovieModel(id=movie_data["id"],
                       title=movie_data["title"],
                       poster = tmdb_poster_url + movie_data["poster_path"] 
                                if movie_data["poster_path"] is not None 
                                else tmdb_poster_url,
                       release_date=movie_data["release_date"])
    
    movie.genres = [GenreModel(id=genre["id"],
                               name=genre["name"])
                    for genre in movie_data["genres"]]

    return movie

def search_movie(name, page=1) -> list[MovieModel]:
    """
    Get movies from TMDB by keywords
    """
    endpoint =  f"search/movie?query={quote(name)}&page={page}"

    data = fetch_tmdb_data(endpoint)
    return create_movie_models(data["results"])

def get_movie_by_id(movie_id: int) -> MovieModel:
    """
    Get movie from TMDB by it's TMDB id
    """
    endpoint =  f"movie/{movie_id}"

    data = fetch_tmdb_data(endpoint)
    return create_full_movie_model(data)

def get_tmdb_genres() -> list[GenreModel]:
    """
    Get all available genres for movies from TMDB
    """
    endpoint =  "genre/movie/list"
    
    data = fetch_tmdb_data(endpoint)
    
    all_genres = [GenreModel(id=genre["id"],
                             name=genre["name"]) 
                  for genre in data["genres"]]
    return all_genres
    
def get_recommendations(movie_id: int) -> list[MovieModel]:
    """
    Get similar movies from TMDB movie id
    """
    endpoint =  f"movie/{movie_id}/recommendations"

    data = fetch_tmdb_data(endpoint)
    return create_movie_models(data["results"])

def get_movies_by_genre(genre: int) -> list[MovieModel]:
    """
    Get best rated movies by genre with >=10_000 votes from TMDB
    """
    endpoint = f"discover/movie?with_genres={genre}&sort_by=vote_average.desc&vote_count.gte=10000"
    
    data = fetch_tmdb_data(endpoint)
    return create_movie_models(data["results"])
