from db import get_db


def get_by_user(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, name, is_public, created_at FROM projects "
        "WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()


def get_by_id(project_id):
    db = get_db()
    return db.execute(
        "SELECT id, name, user_id, is_public, created_at "
        "FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()


def create(user_id, name, is_public=0):
    db = get_db()
    db.execute(
        "INSERT INTO projects (user_id, name, is_public) "
        "VALUES (?, ?, ?)",
        (user_id, name, is_public),
    )
    db.commit()


def update(project_id, name, is_public):
    db = get_db()
    db.execute(
        "UPDATE projects SET name = ?, is_public = ? WHERE id = ?",
        (name, is_public, project_id),
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


def get_public_by_user(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, name, is_public, created_at FROM projects "
        "WHERE user_id = ? AND is_public = 1 "
        "ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()


def search_by_name(user_id, query):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT id, name, is_public, created_at FROM projects "
        "WHERE user_id = ? AND name LIKE ? ORDER BY name",
        (user_id, like),
    ).fetchall()


def search_public(user_id, query):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT p.id, p.name, p.is_public, p.created_at, "
        "       u.id AS owner_id, u.username AS owner_name "
        "FROM projects p "
        "JOIN users u ON p.user_id = u.id "
        "WHERE p.is_public = 1 AND p.user_id != ? "
        "  AND p.name LIKE ? "
        "ORDER BY p.name",
        (user_id, like),
    ).fetchall()
