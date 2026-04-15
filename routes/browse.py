from flask import (
    Blueprint, render_template, request, abort
)
from auth_utils import login_required
from repositories import users, projects_repo, flashcards_repo

browse_bp = Blueprint("browse", __name__)


@browse_bp.route("/users")
@login_required
def search_users():
    query = request.args.get("q", "").strip()
    results = []
    if query:
        results = users.search_by_username(query)
    return render_template(
        "browse/users.html", query=query, results=results
    )


@browse_bp.route("/users/<int:user_id>")
@login_required
def public_profile(user_id):
    user = users.get_by_id(user_id)
    if not user:
        abort(404)
    projects = projects_repo.get_public_by_user(user_id)
    return render_template(
        "browse/profile.html", user=user, projects=projects
    )


@browse_bp.route("/users/<int:user_id>/projects/<int:project_id>")
@login_required
def public_project(user_id, project_id):
    user = users.get_by_id(user_id)
    if not user:
        abort(404)
    project = projects_repo.get_by_id(project_id)
    if (not project
            or project["user_id"] != user_id
            or not project["is_public"]):
        abort(404)
    cards = flashcards_repo.get_by_project(project_id)
    return render_template(
        "browse/project.html",
        user=user,
        project=project,
        cards=cards,
    )
