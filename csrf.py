import secrets
from functools import wraps
from flask import session, request, abort


def generate_csrf_token():
    """Create a CSRF token and store it in the session."""
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


def validate_csrf(f):
    """Decorator that checks the CSRF token on POST requests."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == "POST":
            token = request.form.get("_csrf_token", "")
            if not token or token != session.get("_csrf_token"):
                abort(403)
        return f(*args, **kwargs)
    return decorated
