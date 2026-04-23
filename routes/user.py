from flask import Blueprint, render_template, session
from auth_utils import login_required
from repositories import stats_repo

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]

    total_projects = stats_repo.count_projects(user_id)
    total_cards = stats_repo.count_flashcards(user_id)
    total_sessions = stats_repo.count_completed_sessions(user_id)
    projects = stats_repo.get_projects_with_latest_session(user_id)
    recent_sessions = stats_repo.get_recent_sessions(user_id)

    return render_template(
        "user/profile.html",
        total_projects=total_projects,
        total_cards=total_cards,
        total_sessions=total_sessions,
        projects=projects,
        recent_sessions=recent_sessions,
    )
