import dotenv
import os
import requests

from urllib.parse import quote
from typing import Optional

from .tmdb_models.movie_model import MovieModel

tmdb_base_url =  "https://api.themoviedb.org/3/"

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
    movies = [ MovieModel(id=movie["id"], title=movie["title"], poster="https://image.tmdb.org/t/p/w185/" + movie["poster_path"]) for movie in data["results"] if movie["poster_path"] != None]

    return movies

