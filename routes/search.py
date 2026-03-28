from flask import (
    Blueprint, render_template, request, session,
    flash, redirect, url_for
)
from db import get_db

search_bp = Blueprint("search", __name__)


def login_required(f):
    """Redirect to login if the user is not authenticated."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@search_bp.route("/search")
@login_required
def search():
    query = request.args.get("q", "").strip()
    projects = []
    cards = []

    if query:
        db = get_db()
        like = f"%{query}%"
        projects = db.execute(
            "SELECT id, name, created_at FROM projects "
            "WHERE user_id = ? AND name LIKE ? "
            "ORDER BY name",
            (session["user_id"], like),
        ).fetchall()
        cards = db.execute(
            "SELECT f.id AS card_id, f.front, f.back, "
            "       p.id AS project_id, p.name AS project_name "
            "FROM flashcards f "
            "JOIN projects p ON f.project_id = p.id "
            "WHERE p.user_id = ? "
            "  AND (f.front LIKE ? OR f.back LIKE ?) "
            "ORDER BY p.name, f.id",
            (session["user_id"], like, like),
        ).fetchall()

    return render_template(
        "search/results.html",
        query=query,
        projects=projects,
        cards=cards,
    )
