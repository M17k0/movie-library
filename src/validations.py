import re

from flask import request, flash

regex = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

def validate_sign_up(user) -> bool:
    if user:
        flash(f"Email: {user.email} already in use. Please log in.", category="error")
        return False
    
    email = request.form.get("email") or ""

    if not re.fullmatch(regex, email):
        flash("Enter a valid email address.", category="error")
        return False

    password1 = request.form.get("password1") or ""
    password2 = request.form.get("password2") or ""

    if password1 != password2:
        flash("Passwords don't match.", category="error")
        return False
    elif len(password1) < 7:
        flash("Password should be at least 8 symbols.", category="error")
        return False
    
    return True
    
def validate_login() -> bool:
    ...