from flask_login import UserMixin
from sqlalchemy.sql import func

from .setup import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    watched_movies = db.relationship("Watched")
    watchlist = db.relationship("Watchlist")

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String(256))
    poster = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)

    movie_genres = db.relationship("MovieGenre")

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    name = db.Column(db.String(64))

    movie_genres = db.relationship("MovieGenre")

class MovieGenre(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), primary_key=True)

class Watched(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    date_watched = db.Column(db.DateTime, default=func.now())

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))