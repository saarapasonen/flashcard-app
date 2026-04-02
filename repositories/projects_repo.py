from db import get_db


def get_by_user(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, name, created_at FROM projects "
        "WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()


def get_by_id(project_id):
    db = get_db()
    return db.execute(
        "SELECT id, name, user_id, created_at FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()


def create(user_id, name):
    db = get_db()
    db.execute(
        "INSERT INTO projects (user_id, name) VALUES (?, ?)",
        (user_id, name),
    )
    db.commit()


def update_name(project_id, name):
    db = get_db()
    db.execute(
        "UPDATE projects SET name = ? WHERE id = ?",
        (name, project_id),
    )
    db.commit()


def delete(project_id):
    db = get_db()
    db.execute(
        "DELETE FROM flashcards WHERE project_id = ?",
        (project_id,),
    )
    db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    db.commit()


def search_by_name(user_id, query):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT id, name, created_at FROM projects "
        "WHERE user_id = ? AND name LIKE ? ORDER BY name",
        (user_id, like),
    ).fetchall()
