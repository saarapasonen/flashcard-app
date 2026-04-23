from db import get_db


def count_projects(user_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(id) AS total FROM projects "
        "WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return row["total"]


def count_flashcards(user_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(f.id) AS total "
        "FROM flashcards f "
        "JOIN projects p ON f.project_id = p.id "
        "WHERE p.user_id = ?",
        (user_id,),
    ).fetchone()
    return row["total"]


def count_completed_sessions(user_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(id) AS total FROM study_sessions "
        "WHERE user_id = ? AND status = 'completed'",
        (user_id,),
    ).fetchone()
    return row["total"]


def get_projects_with_latest_session(user_id):
    db = get_db()
    return db.execute(
        "SELECT p.id, p.name, p.created_at, "
        "       s.correct, s.total_cards, "
        "       s.created_at AS session_date "
        "FROM projects p "
        "LEFT JOIN study_sessions s ON s.id = ("
        "  SELECT s2.id FROM study_sessions s2 "
        "  WHERE s2.project_id = p.id "
        "    AND s2.status = 'completed' "
        "  ORDER BY s2.created_at DESC LIMIT 1"
        ") "
        "WHERE p.user_id = ? "
        "ORDER BY p.created_at DESC",
        (user_id,),
    ).fetchall()


def get_recent_sessions(user_id, limit=10):
    db = get_db()
    return db.execute(
        "SELECT s.id, s.total_cards, s.correct, s.created_at, "
        "       p.name AS project_name, p.id AS project_id "
        "FROM study_sessions s "
        "JOIN projects p ON s.project_id = p.id "
        "WHERE s.user_id = ? AND s.status = 'completed' "
        "ORDER BY s.created_at DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
