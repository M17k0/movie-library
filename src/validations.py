import re
from werkzeug.security import check_password_hash

from flask import request, flash

regex = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

def is_sig_up_info_valid(user) -> bool:
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
    
def is_login_info_valid(user) -> bool:
        if user:
            password = request.form.get("password") or ""
            if check_password_hash(user.password, password):
                return True 
            else:
                flash("Email and password do not match. Try again.", category="error")
        else:
            flash("No user with this email. Sign up.", category="error")
            
        return False