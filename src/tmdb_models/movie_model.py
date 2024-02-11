"""
TMDB models
"""
from dataclasses import dataclass, field

@dataclass
class GenreModel:
    id: int
    name: str

@dataclass
class MovieModel:
    id: int
    title: str
    poster: str
    release_date: str
    genres: list[GenreModel] = field(default_factory=list)