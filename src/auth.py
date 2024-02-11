"""
Handles routes for authentication
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from .validations import is_sign_up_info_valid, is_login_info_valid

auth = Blueprint("auth", __name__, template_folder="../templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    from .models import User

    if request.method == "POST":
        email = request.form.get("email")

        user = (User.query
                .filter_by(email=email)
                .first())
        if is_login_info_valid(user):
                login_user(user, remember=True)
                flash("Logged in successfully.", category="success")
                return redirect(url_for("views.home"))

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    from .models import User

    if request.method == "POST":
        data = request.form
        if not is_sign_up_info_valid((User.query
                                      .filter_by(email=data.get('email'))
                                      .first())):
            return render_template("sign_up.html", user=current_user)

        email = request.form.get("email")
        password = request.form.get("password1") or ""
        password_hash = generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=16)

        new_user = User()
        new_user.email = email
        new_user.password = password_hash

        from .setup import db

        login_user(new_user, remember=True)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", category="success")
        return redirect(url_for("views.home"))
    
    return render_template("sign_up.html", user=current_user)