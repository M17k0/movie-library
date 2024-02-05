from flask import Blueprint, render_template, current_app
import os

views = Blueprint("views", __name__, template_folder='templates')

@views.route('/')
def home():
    # return f"{current_app.template_folder}"
    return render_template("home.html")