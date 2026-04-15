from db import get_db
from werkzeug.security import generate_password_hash


def find_by_username(username):
    db = get_db()
    return db.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,),
    ).fetchone()


def create(username, password):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password, method="pbkdf2:sha256")),
    )
    db.commit()


def search_by_username(query):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT id, username FROM users "
        "WHERE username LIKE ? ORDER BY username",
        (like,),
    ).fetchall()


def get_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, username FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
