from flask import Blueprint, render_template, current_app
import os
from flask_login import current_user, login_required

views = Blueprint("views", __name__, template_folder="../templates/")

@views.route("/")
def main_route():
    if current_user.is_authenticated:
         return render_template("home.html", user=current_user)
    else:
         return render_template("login.html", user=current_user)

@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)