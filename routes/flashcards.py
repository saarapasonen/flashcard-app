from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from csrf import validate_csrf
from auth_utils import login_required
from repositories import projects_repo, flashcards_repo

flashcards_bp = Blueprint("flashcards", __name__)


def get_owned_project(project_id):
    """Return the project row if the current user owns it."""
    project = projects_repo.get_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        abort(404)
    return project


@flashcards_bp.route(
    "/projects/<int:project_id>/cards/create",
    methods=["GET", "POST"],
)
@login_required
@validate_csrf
def create_card(project_id):
    project = get_owned_project(project_id)

    if request.method == "POST":
        front = request.form.get("front", "").strip()
        back = request.form.get("back", "").strip()
        difficulty = request.form.get("difficulty", "medium")
        if difficulty not in ("easy", "medium", "hard"):
            difficulty = "medium"

        if not front or not back:
            flash("Both front and back are required.", "error")
            return render_template(
                "flashcards/create.html", project=project
            )

        flashcards_repo.create(project_id, front, back, difficulty)
        flash("Flashcard added.", "success")
        return redirect(
            url_for(
                "projects.view_project", project_id=project_id
            )
        )

    return render_template(
        "flashcards/create.html", project=project
    )


@flashcards_bp.route(
    "/projects/<int:project_id>/cards/<int:card_id>/edit",
    methods=["GET", "POST"],
)
@login_required
@validate_csrf
def edit_card(project_id, card_id):
    project = get_owned_project(project_id)
    card = flashcards_repo.get_by_id(card_id, project_id)

    if not card:
        abort(404)

    if request.method == "POST":
        front = request.form.get("front", "").strip()
        back = request.form.get("back", "").strip()
        difficulty = request.form.get("difficulty", "medium")
        if difficulty not in ("easy", "medium", "hard"):
            difficulty = "medium"

        if not front or not back:
            flash("Both front and back are required.", "error")
            return render_template(
                "flashcards/edit.html",
                project=project,
                card=card,
            )

        flashcards_repo.update(card_id, front, back, difficulty)
        flash("Flashcard updated.", "success")
        return redirect(
            url_for(
                "projects.view_project", project_id=project_id
            )
        )

    return render_template(
        "flashcards/edit.html", project=project, card=card
    )


@flashcards_bp.route(
    "/projects/<int:project_id>/cards/<int:card_id>/delete",
    methods=["POST"],
)
@login_required
@validate_csrf
def delete_card(project_id, card_id):
    get_owned_project(project_id)
    card = flashcards_repo.get_by_id(card_id, project_id)

    if not card:
        abort(404)

    flashcards_repo.delete(card_id)
    flash("Flashcard deleted.", "success")
    return redirect(
        url_for("projects.view_project", project_id=project_id)
    )
