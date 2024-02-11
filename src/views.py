"""
Handles routes for logging watched movies, managing watchlists,
discovering movies by genre, and finding similar movies using the TMDB API.
"""
from flask import Blueprint, render_template, current_app, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from datetime import datetime

from .tmdb_interface import search_movie, get_movie_by_id, get_tmdb_genres, get_movies_by_genre, get_reccomendations
from .setup import db
from .models import Watched, Watchlist, Genre, Movie, MovieGenre

views = Blueprint("views", __name__, template_folder="../templates/")

@views.route("/watched", methods=["GET"])
@login_required
def watched():
    watched_movies = (Watched.query
                      .filter_by(user_id=current_user.id)
                      .order_by(Watched.date_watched.desc())
                      .all())
    
    return render_template("watched.html",
                           user=current_user,
                           watched_movies=watched_movies)

@views.route("/watchlist")
def watchlist():
    from .models import Watchlist

    watchlist = (Watchlist.query
                 .filter_by(user_id=current_user.id)
                 .order_by(Watchlist.id.desc())
                 .all())
    
    return render_template("watchlist.html",
                           user=current_user,
                           watchlist=watchlist)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        movie_title = request.form.get("movie_title")
        if movie_title:
            try:
                search_results = search_movie(movie_title)
            except:
                flash("TMDB API is down!", category="error")
                return render_template("home.html", user=current_user)
            
            return render_template("home.html",
                                   user=current_user,
                                   search_results=search_results)
        
    return render_template("home.html", user=current_user)

@views.route("/log/<id>", methods=["GET", "POST"])
@login_required
def log(id):
    if request.method == "POST":
        try:
            movie = get_movie_by_id(id)
        except:
            flash("TMDB API is down!", category="error")
            return redirect(url_for("views.home"))
        
        db_genres = []
        for genre in movie.genres:
            db_genre = (Genre.query
                        .filter_by(tmdb_id=genre.id)
                        .first())
            if not db_genre:
                db_genre = Genre()
                db_genre.tmdb_id = genre.id
                db_genre.name = genre.name
                db.session.add(db_genre)
                db.session.flush()
            db_genres.append(db_genre)
        
        db_movie = (Movie.query
                    .filter_by(tmdb_id=movie.id)
                    .first())
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
        
        return redirect(url_for("views.watched"))
    
    try:
        movie = get_movie_by_id(id)
    except:
        flash("TMDB API is down!", category="error")
        return redirect(url_for("views.home"))
        
    return render_template("log.html", 
                           user=current_user, 
                           movie=movie)

@views.route("/remove-log/<id>", methods=["POST"])
@login_required
def remove_log(id):
    db_watched = (Watched.query
                  .filter_by(id=id)
                  .first())
    
    if not db_watched:
        abort(400)
    
    db.session.delete(db_watched)
    db.session.commit()
    
    return redirect(url_for("views.watched"))

@views.route("/add-to-watchlist/<id>", methods=["POST"])
@login_required
def add_to_watchlist(id):
    try:
        movie = get_movie_by_id(id)
    except:
        flash("TMDB API is down!", category="error")
        return redirect(url_for("views.home"))
    
    db_genres = []
    for genre in movie.genres:
        db_genre = (Genre.query
                    .filter_by(tmdb_id=genre.id)
                    .first())
        if not db_genre:
            db_genre = Genre()
            db_genre.tmdb_id = genre.id
            db_genre.name = genre.name
            db.session.add(db_genre)
            db.session.flush()
        db_genres.append(db_genre)
    
    db_movie = (Movie.query
                .filter_by(tmdb_id=movie.id)
                .first())
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
    
    db_watched = (Watched.query
                  .filter_by(movie_id=db_movie.id)
                  .first() )   
    if db_watched:
        flash("Movie already watched!", category="error")
        return redirect(url_for("views.home"))
    
    db_watchlist = (Watchlist.query
                    .filter_by(movie_id=db_movie.id)
                    .first())
    if db_watchlist:
        flash("Movie already in watchlist!", category="error")
        return redirect(url_for("views.home"))
    
    db_watchlist = Watchlist()
    db_watchlist.user_id = current_user.id
    db_watchlist.movie_id = db_movie.id
    
    db.session.add(db_watchlist)
    db.session.commit()
    
    return redirect(url_for("views.watchlist"))
      
@views.route("/remove-watchlist/<id>", methods=["POST"])
@login_required
def remove_watchlsit(id):
    db_watchlist = (Watchlist.query
                    .filter_by(id=id)
                    .first()) 
    if not db_watchlist:
        abort(400)
    
    db.session.delete(db_watchlist)
    db.session.commit()
    
    return redirect(url_for("views.watchlist"))  

@views.route("/discover", methods=["GET", "POST"])
@login_required
def discover():
    try:
        genres = get_tmdb_genres()
    except:
        flash("TMDB API is down!", category="error")
        return redirect(url_for("views.home"))
    
    if request.method == "POST":
        genre_id = (request.form.get("genre_id") or "0")
        movies = get_movies_by_genre(int(genre_id))
        
        return render_template("discover.html",
                               user=current_user,
                               genres=genres,
                               selected_genre_id=genre_id,
                               discover_results=movies)
    
    return render_template("discover.html",
                           user=current_user,
                           genres=genres)

@views.route("/similar/<id>")
@login_required
def similar(id):
    try:
        similar_movies = get_reccomendations(id)
    except:
        flash("TMDB API is down!", category="error")
        return redirect(url_for("views.home"))

    return render_template("similar.html",
                           user=current_user,
                           similar_movies=similar_movies)
    