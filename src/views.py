from flask import Blueprint, render_template, current_app, request, redirect, url_for
import os
from flask_login import current_user, login_required
from datetime import datetime

from .tmdb_interface import search_movie, get_movie_by_id
from .setup import db
from .models import User, Watched, Watchlist, Genre, Movie, MovieGenre

views = Blueprint("views", __name__, template_folder="../templates/")

@views.route('/watched')
def watched():
    from .models import Watched

    watched_movies = Watched.query.all()
    return render_template('watched.html', user=current_user, watched_movies=watched_movies)

@views.route('/watchlist')
def watchlist():
    from .models import Watchlist

    watchlist = Watchlist.query.all()
    return render_template('watchlist.html', user=current_user, watched_movies=watchlist)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        movie_title = request.form.get("movie_title")
        if movie_title:
            search_results = search_movie(movie_title)
            return render_template("home.html", user=current_user, search_results=search_results)
        
    return render_template("home.html", user=current_user)

@views.route("/log/<id>", methods=["GET", "POST"])
@login_required
def log(id):
    if request.method == "POST":
        movie = get_movie_by_id(id)
        
        db_genres = []
        for genre in movie.genres:
            db_genre = Genre.query.filter_by(tmdb_id=genre.id).first()
            if not db_genre:
                db_genre = Genre()
                db_genre.tmdb_id = genre.id
                db_genre.name = genre.name
                db.session.add(db_genre)
                db.session.flush()
            db_genres.append(db_genre)
        
        db_movie = Movie.query.filter_by(tmdb_id=movie.id).first()
        if not db_movie:
            db_movie = Movie()
            db_movie.tmdb_id = movie.id
            db_movie.title = movie.title
            db_movie.poster = movie.poster
            release_date = datetime.strptime(movie.release_date, "%Y-%m-%d") 
            db_movie.release_date = release_date
            db.session.add(db_movie)
            db.session.flush()
            
            for genre in db_genres:
                movie_genre = MovieGenre()
                movie_genre.movie_id = db_movie.id
                movie_genre.genre_id = genre.id
                db.session.add(movie_genre)
                db.session.flush()
            
                
        db_watched = Watched()
        db_watched.user_id = current_user.id
        db_watched.movie_id = db_movie.id
        db_watched.rating = request.form.get("rating")
        db_watched.review = request.form.get("review")
        watched_date = datetime.strptime(request.form.get("date_watched") or "", "%Y-%m-%d") 
        db_watched.date_watched = watched_date
        
        db.session.add(db_watched)
        db.session.commit()
        
        return redirect(url_for("views.home"))
    
    movie = get_movie_by_id(id)
    return render_template("log.html", user=current_user, movie=movie)