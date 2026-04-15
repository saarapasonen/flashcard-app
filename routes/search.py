from flask import (
    Blueprint, render_template, request, session
)
from auth_utils import login_required
from repositories import projects_repo, flashcards_repo, users

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@login_required
def search():
    query = request.args.get("q", "").strip()
    my_projects = []
    cards = []
    public_projects = []
    found_users = []

    if query:
        my_projects = projects_repo.search_by_name(
            session["user_id"], query
        )
        cards = flashcards_repo.search(session["user_id"], query)
        public_projects = projects_repo.search_public(
            session["user_id"], query
        )
        found_users = users.search_by_username(query)

    return render_template(
        "search/results.html",
        query=query,
        my_projects=my_projects,
        cards=cards,
        public_projects=public_projects,
        found_users=found_users,
    )
