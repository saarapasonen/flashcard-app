from db import get_db


def create_session(user_id, project_id, total_cards):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO study_sessions "
        "(user_id, project_id, total_cards) "
        "VALUES (?, ?, ?)",
        (user_id, project_id, total_cards),
    )
    db.commit()
    return cursor.lastrowid


def get_by_id(session_id):
    db = get_db()
    return db.execute(
        "SELECT id, user_id, project_id, total_cards, "
        "       correct, completed, created_at "
        "FROM study_sessions WHERE id = ?",
        (session_id,),
    ).fetchone()


def add_answer(session_id, card_id, known):
    db = get_db()
    db.execute(
        "INSERT INTO session_answers (session_id, card_id, known) "
        "VALUES (?, ?, ?)",
        (session_id, card_id, 1 if known else 0),
    )
    db.commit()


def count_answers(session_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(id) AS total, "
        "       SUM(known) AS correct "
        "FROM session_answers WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    return row["total"], row["correct"] or 0


def complete_session(session_id, correct):
    db = get_db()
    db.execute(
        "UPDATE study_sessions SET completed = 1, correct = ? "
        "WHERE id = ?",
        (correct, session_id),
    )
    db.commit()


def get_answered_card_ids(session_id):
    db = get_db()
    rows = db.execute(
        "SELECT card_id FROM session_answers "
        "WHERE session_id = ?",
        (session_id,),
    ).fetchall()
    return [r["card_id"] for r in rows]


def get_latest_session(user_id, project_id):
    db = get_db()
    return db.execute(
        "SELECT id, user_id, project_id, total_cards, "
        "       correct, completed, created_at "
        "FROM study_sessions "
        "WHERE user_id = ? AND project_id = ? AND completed = 1 "
        "ORDER BY created_at DESC LIMIT 1",
        (user_id, project_id),
    ).fetchone()


def get_unknown_card_ids(session_id):
    db = get_db()
    rows = db.execute(
        "SELECT card_id FROM session_answers "
        "WHERE session_id = ? AND known = 0",
        (session_id,),
    ).fetchall()
    return [r["card_id"] for r in rows]
