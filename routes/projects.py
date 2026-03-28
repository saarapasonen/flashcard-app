from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from db import get_db
from csrf import validate_csrf

projects_bp = Blueprint("projects", __name__)


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


@projects_bp.route("/")
@login_required
def list_projects():
    db = get_db()
    projects = db.execute(
        "SELECT id, name, created_at FROM projects "
        "WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],),
    ).fetchall()
    return render_template("projects/list.html", projects=projects)


@projects_bp.route("/projects/create", methods=["GET", "POST"])
@login_required
@validate_csrf
def create_project():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Project name is required.", "error")
            return render_template("projects/create.html")

        db = get_db()
        db.execute(
            "INSERT INTO projects (user_id, name) VALUES (?, ?)",
            (session["user_id"], name),
        )
        db.commit()
        flash("Project created.", "success")
        return redirect(url_for("projects.list_projects"))

    return render_template("projects/create.html")


@projects_bp.route("/projects/<int:project_id>")
@login_required
def view_project(project_id):
    db = get_db()
    project = db.execute(
        "SELECT id, name, user_id, created_at FROM projects "
        "WHERE id = ?",
        (project_id,),
    ).fetchone()

    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    cards = db.execute(
        "SELECT id, front, back FROM flashcards "
        "WHERE project_id = ? ORDER BY id",
        (project_id,),
    ).fetchall()

    return render_template(
        "projects/view.html", project=project, cards=cards
    )


@projects_bp.route(
    "/projects/<int:project_id>/edit", methods=["GET", "POST"]
)
@login_required
@validate_csrf
def edit_project(project_id):
    db = get_db()
    project = db.execute(
        "SELECT id, name, user_id FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()

    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Project name is required.", "error")
            return render_template(
                "projects/edit.html", project=project
            )

        db.execute(
            "UPDATE projects SET name = ? WHERE id = ?",
            (name, project_id),
        )
        db.commit()
        flash("Project updated.", "success")
        return redirect(
            url_for("projects.view_project", project_id=project_id)
        )

    return render_template("projects/edit.html", project=project)


@projects_bp.route(
    "/projects/<int:project_id>/delete", methods=["POST"]
)
@login_required
@validate_csrf
def delete_project(project_id):
    db = get_db()
    project = db.execute(
        "SELECT id, user_id FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()

    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    db.execute(
        "DELETE FROM flashcards WHERE project_id = ?",
        (project_id,),
    )
    db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    db.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("projects.list_projects"))
