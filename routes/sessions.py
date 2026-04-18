from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from csrf import validate_csrf
from auth_utils import login_required
from repositories import (
    projects_repo, flashcards_repo, sessions_repo
)

sessions_bp = Blueprint("sessions", __name__)


def get_owned_project(project_id):
    """Return the project row if the current user owns it."""
    project = projects_repo.get_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        abort(404)
    return project


@sessions_bp.route(
    "/projects/<int:project_id>/study",
    methods=["POST"],
)
@login_required
@validate_csrf
def start_session(project_id):
    get_owned_project(project_id)
    cards = flashcards_repo.get_by_project(project_id)

    if not cards:
        flash("No cards to study.", "error")
        return redirect(
            url_for(
                "projects.view_project", project_id=project_id
            )
        )

    session_id = sessions_repo.create_session(
        session["user_id"], project_id, len(cards)
    )
    return redirect(
        url_for(
            "sessions.study_card",
            project_id=project_id,
            session_id=session_id,
        )
    )


@sessions_bp.route(
    "/projects/<int:project_id>/continue",
    methods=["POST"],
)
@login_required
@validate_csrf
def continue_session(project_id):
    get_owned_project(project_id)
    latest = sessions_repo.get_latest_session(
        session["user_id"], project_id
    )

    if not latest:
        flash("No previous session to continue from.", "error")
        return redirect(
            url_for(
                "projects.view_project", project_id=project_id
            )
        )

    unseen_ids = sessions_repo.get_unseen_card_ids(
        latest["id"], project_id
    )
    unknown_ids = sessions_repo.get_unknown_card_ids(latest["id"])
    card_ids = unseen_ids + unknown_ids

    if not card_ids:
        flash(
            "You knew all cards in your last session!", "success"
        )
        return redirect(
            url_for(
                "projects.view_project", project_id=project_id
            )
        )

    session_id = sessions_repo.create_session(
        session["user_id"], project_id, len(card_ids)
    )
    sessions_repo.add_session_cards(session_id, card_ids)

    return redirect(
        url_for(
            "sessions.study_card",
            project_id=project_id,
            session_id=session_id,
        )
    )


@sessions_bp.route(
    "/projects/<int:project_id>/study/<int:session_id>",
)
@login_required
def study_card(project_id, session_id):
    project = get_owned_project(project_id)
    study = sessions_repo.get_by_id(session_id)

    if not study or study["user_id"] != session["user_id"]:
        abort(404)

    session_card_ids = sessions_repo.get_session_card_ids(
        session_id
    )
    all_cards = flashcards_repo.get_by_project(project_id)

    if session_card_ids:
        cards = [
            c for c in all_cards if c["id"] in session_card_ids
        ]
    else:
        cards = all_cards

    answered_ids = sessions_repo.get_answered_card_ids(session_id)
    remaining = [c for c in cards if c["id"] not in answered_ids]

    if not remaining:
        return redirect(
            url_for(
                "sessions.session_results",
                project_id=project_id,
                session_id=session_id,
            )
        )

    card = remaining[0]
    progress = len(answered_ids) + 1
    total = len(cards)

    return render_template(
        "sessions/study.html",
        project=project,
        card=card,
        session_id=session_id,
        progress=progress,
        total=total,
        revealed=False,
    )


@sessions_bp.route(
    "/projects/<int:project_id>/study/<int:session_id>/reveal",
    methods=["POST"],
)
@login_required
@validate_csrf
def reveal_card(project_id, session_id):
    project = get_owned_project(project_id)
    study = sessions_repo.get_by_id(session_id)

    if not study or study["user_id"] != session["user_id"]:
        abort(404)

    card_id = request.form.get("card_id", type=int)
    card = flashcards_repo.get_by_id(card_id, project_id)
    if not card:
        abort(404)

    session_card_ids = sessions_repo.get_session_card_ids(
        session_id
    )
    all_cards = flashcards_repo.get_by_project(project_id)
    if session_card_ids:
        cards = [
            c for c in all_cards if c["id"] in session_card_ids
        ]
    else:
        cards = all_cards

    answered_ids = sessions_repo.get_answered_card_ids(session_id)
    progress = len(answered_ids) + 1
    total = len(cards)

    return render_template(
        "sessions/study.html",
        project=project,
        card=card,
        session_id=session_id,
        progress=progress,
        total=total,
        revealed=True,
    )


@sessions_bp.route(
    "/projects/<int:project_id>/study/<int:session_id>/answer",
    methods=["POST"],
)
@login_required
@validate_csrf
def answer_card(project_id, session_id):
    get_owned_project(project_id)
    study = sessions_repo.get_by_id(session_id)

    if not study or study["user_id"] != session["user_id"]:
        abort(404)

    card_id = request.form.get("card_id", type=int)
    known = request.form.get("known") == "1"

    sessions_repo.add_answer(session_id, card_id, known)

    return redirect(
        url_for(
            "sessions.study_card",
            project_id=project_id,
            session_id=session_id,
        )
    )


@sessions_bp.route(
    "/projects/<int:project_id>/study/<int:session_id>/save",
    methods=["POST"],
)
@login_required
@validate_csrf
def save_session(project_id, session_id):
    get_owned_project(project_id)
    study = sessions_repo.get_by_id(session_id)

    if not study or study["user_id"] != session["user_id"]:
        abort(404)

    flash("Session saved. You can resume it later.", "success")
    return redirect(
        url_for(
            "projects.view_project", project_id=project_id
        )
    )


@sessions_bp.route(
    "/projects/<int:project_id>/study/<int:session_id>/results",
)
@login_required
def session_results(project_id, session_id):
    project = get_owned_project(project_id)
    study = sessions_repo.get_by_id(session_id)

    if not study or study["user_id"] != session["user_id"]:
        abort(404)

    answered, correct = sessions_repo.count_answers(session_id)

    if (study["status"] == "in_progress"
            and answered == study["total_cards"]):
        sessions_repo.complete_session(session_id, correct)

    percentage = (
        round(correct / answered * 100) if answered else 0
    )

    return render_template(
        "sessions/results.html",
        project=project,
        correct=correct,
        total=answered,
        percentage=percentage,
        session_id=session_id,
    )
