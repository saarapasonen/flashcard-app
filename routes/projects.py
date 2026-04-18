from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from csrf import validate_csrf
from auth_utils import login_required
from repositories import projects_repo, flashcards_repo

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/")
@login_required
def list_projects():
    projects = projects_repo.get_by_user(session["user_id"])
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

        is_public = 1 if request.form.get("is_public") else 0
        projects_repo.create(session["user_id"], name, is_public)
        flash("Project created.", "success")
        return redirect(url_for("projects.list_projects"))

    return render_template("projects/create.html")


@projects_bp.route("/projects/<int:project_id>")
@login_required
def view_project(project_id):
    project = projects_repo.get_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    per_page = 20
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    difficulty = request.args.get("difficulty", "").strip()
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = None

    total = flashcards_repo.count_by_project(
        project_id, difficulty
    )
    total_pages = max(1, (total + per_page - 1) // per_page)
    if page > total_pages:
        page = total_pages
    offset = (page - 1) * per_page

    cards = flashcards_repo.get_page(
        project_id, per_page, offset, difficulty
    )
    return render_template(
        "projects/view.html",
        project=project,
        cards=cards,
        page=page,
        total_pages=total_pages,
        difficulty=difficulty or "",
    )


@projects_bp.route(
    "/projects/<int:project_id>/edit", methods=["GET", "POST"]
)
@login_required
@validate_csrf
def edit_project(project_id):
    project = projects_repo.get_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Project name is required.", "error")
            return render_template(
                "projects/edit.html", project=project
            )

        is_public = 1 if request.form.get("is_public") else 0
        projects_repo.update(project_id, name, is_public)
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
    project = projects_repo.get_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        abort(404)

    projects_repo.delete(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for("projects.list_projects"))
