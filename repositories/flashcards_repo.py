from db import get_db


def get_by_project(project_id):
    db = get_db()
    return db.execute(
        "SELECT id, front, back, difficulty FROM flashcards "
        "WHERE project_id = ? ORDER BY id",
        (project_id,),
    ).fetchall()


def get_page(project_id, limit, offset, difficulty=None):
    db = get_db()
    if difficulty:
        return db.execute(
            "SELECT id, front, back, difficulty FROM flashcards "
            "WHERE project_id = ? AND difficulty = ? "
            "ORDER BY id LIMIT ? OFFSET ?",
            (project_id, difficulty, limit, offset),
        ).fetchall()
    return db.execute(
        "SELECT id, front, back, difficulty FROM flashcards "
        "WHERE project_id = ? "
        "ORDER BY id LIMIT ? OFFSET ?",
        (project_id, limit, offset),
    ).fetchall()


def count_by_project(project_id, difficulty=None):
    db = get_db()
    if difficulty:
        row = db.execute(
            "SELECT COUNT(id) AS total FROM flashcards "
            "WHERE project_id = ? AND difficulty = ?",
            (project_id, difficulty),
        ).fetchone()
    else:
        row = db.execute(
            "SELECT COUNT(id) AS total FROM flashcards "
            "WHERE project_id = ?",
            (project_id,),
        ).fetchone()
    return row["total"]


def get_by_id(card_id, project_id):
    db = get_db()
    return db.execute(
        "SELECT id, front, back, project_id, difficulty "
        "FROM flashcards "
        "WHERE id = ? AND project_id = ?",
        (card_id, project_id),
    ).fetchone()


def create(project_id, front, back, difficulty):
    db = get_db()
    db.execute(
        "INSERT INTO flashcards (project_id, front, back, difficulty) "
        "VALUES (?, ?, ?, ?)",
        (project_id, front, back, difficulty),
    )
    db.commit()


def update(card_id, front, back, difficulty):
    db = get_db()
    db.execute(
        "UPDATE flashcards SET front = ?, back = ?, difficulty = ? "
        "WHERE id = ?",
        (front, back, difficulty, card_id),
    )
    db.commit()


def delete(card_id):
    db = get_db()
    db.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    db.commit()


def search(user_id, query):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT f.id AS card_id, f.front, f.back, "
        "       f.difficulty, "
        "       p.id AS project_id, p.name AS project_name "
        "FROM flashcards f "
        "JOIN projects p ON f.project_id = p.id "
        "WHERE p.user_id = ? "
        "  AND (f.front LIKE ? OR f.back LIKE ?) "
        "ORDER BY p.name, f.id",
        (user_id, like, like),
    ).fetchall()
