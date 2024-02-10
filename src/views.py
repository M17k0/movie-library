from flask import Blueprint, render_template, current_app, request
import os
from flask_login import current_user, login_required

from .tmdb_interface import search_movie
from .setup import db
from .models import User, Watched, Watchlist

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
