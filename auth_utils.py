from functools import wraps
from flask import session, flash, redirect, url_for


def login_required(f):
    """Redirect to login if the user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
