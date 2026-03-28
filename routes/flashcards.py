from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from db import get_db
from csrf import validate_csrf

flashcards_bp = Blueprint("flashcards", __name__)


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


def get_owned_project(project_id):
    """Return the project row if the current user owns it."""
    db = get_db()
    project = db.execute(
        "SELECT id, name, user_id FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()
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

        if not front or not back:
            flash("Both front and back are required.", "error")
            return render_template(
                "flashcards/create.html", project=project
            )

        db = get_db()
        db.execute(
            "INSERT INTO flashcards (project_id, front, back) "
            "VALUES (?, ?, ?)",
            (project_id, front, back),
        )
        db.commit()
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
    db = get_db()
    card = db.execute(
        "SELECT id, front, back, project_id FROM flashcards "
        "WHERE id = ? AND project_id = ?",
        (card_id, project_id),
    ).fetchone()

    if not card:
        abort(404)

    if request.method == "POST":
        front = request.form.get("front", "").strip()
        back = request.form.get("back", "").strip()

        if not front or not back:
            flash("Both front and back are required.", "error")
            return render_template(
                "flashcards/edit.html",
                project=project,
                card=card,
            )

        db.execute(
            "UPDATE flashcards SET front = ?, back = ? "
            "WHERE id = ?",
            (front, back, card_id),
        )
        db.commit()
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
    project = get_owned_project(project_id)
    db = get_db()
    card = db.execute(
        "SELECT id FROM flashcards "
        "WHERE id = ? AND project_id = ?",
        (card_id, project_id),
    ).fetchone()

    if not card:
        abort(404)

    db.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    db.commit()
    flash("Flashcard deleted.", "success")
    return redirect(
        url_for("projects.view_project", project_id=project_id)
    )
