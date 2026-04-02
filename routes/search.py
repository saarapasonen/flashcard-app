from flask import (
    Blueprint, render_template, request, session
)
from auth_utils import login_required
from repositories import projects_repo, flashcards_repo

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@login_required
def search():
    query = request.args.get("q", "").strip()
    projects = []
    cards = []

    if query:
        projects = projects_repo.search_by_name(
            session["user_id"], query
        )
        cards = flashcards_repo.search(session["user_id"], query)

    return render_template(
        "search/results.html",
        query=query,
        projects=projects,
        cards=cards,
    )
