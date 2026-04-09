CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS flashcards (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    front      TEXT NOT NULL,
    back       TEXT NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'medium'
        CHECK (difficulty IN ('easy', 'medium', 'hard'))
);

CREATE INDEX IF NOT EXISTS idx_projects_user_id
    ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_project
    ON flashcards(project_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_front
    ON flashcards(front);
