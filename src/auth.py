from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .validations import validate_sign_up

auth = Blueprint("auth", __name__, template_folder="../templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    from .models import User

    if request.method == "POST":
        data = request.form
        if not validate_sign_up(User.query.filter_by(email=data.get('email')).first()):
            return render_template("sign_up.html")

        # everything is valid
        email = request.form.get("email")
        password = request.form.get("password1") or ""
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        new_user = User()
        new_user.email = email
        new_user.password = password_hash

        from .setup import db 

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", category="success")
        return redirect(url_for("views.home"))
    
    return render_template("sign_up.html")
