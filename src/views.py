from flask import Blueprint, render_template, current_app
import os
from flask_login import current_user, login_required

views = Blueprint("views", __name__, template_folder="../templates/")

# @views.route("/", methods=["GET", "POST"])
# def main_route():
#     if current_user.is_authenticated:
#          return render_template("home.html", user=current_user)
#     else:
#          return render_template("login.html", user=current_user)

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

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)