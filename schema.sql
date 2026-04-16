CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    name       TEXT NOT NULL,
    is_public  INTEGER NOT NULL DEFAULT 0,
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

CREATE TABLE IF NOT EXISTS study_sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    project_id  INTEGER NOT NULL REFERENCES projects(id),
    total_cards INTEGER NOT NULL,
    correct     INTEGER NOT NULL DEFAULT 0,
    status      TEXT NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('in_progress', 'completed')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS session_answers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES study_sessions(id),
    card_id    INTEGER NOT NULL REFERENCES flashcards(id),
    known      INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sessions_user
    ON study_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project
    ON study_sessions(project_id);
CREATE TABLE IF NOT EXISTS session_cards (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES study_sessions(id),
    card_id    INTEGER NOT NULL REFERENCES flashcards(id)
);

CREATE INDEX IF NOT EXISTS idx_session_answers_session
    ON session_answers(session_id);
CREATE INDEX IF NOT EXISTS idx_session_cards_session
    ON session_cards(session_id);

CREATE INDEX IF NOT EXISTS idx_projects_user_id
    ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_project
    ON flashcards(project_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_front
    ON flashcards(front);
