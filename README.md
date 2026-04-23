# Flashcards

A web application for creating and studying flashcards, built with Python and Flask.

## Features

- User registration and login with secure password hashing
- Create, edit, and delete projects (collections of flashcards)
- Public and private projects — public projects are visible to other users
- Create, edit, and delete flashcards with Easy / Medium / Hard difficulty tags
- Study sessions — go through cards one by one, reveal the answer, mark as known or unknown
- Save progress mid-session and continue later
- Smart continue — repeats unseen and unknown cards from the previous session
- User profile page with stats: total projects, flashcards, completed sessions
- Unified search across own projects, flashcards, other users, and public projects
- Pagination with difficulty filtering on the flashcard list (20 cards per page)

## Requirements

- Python 3.8+
- Flask

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Flask
pip install flask

# Initialize the database
sqlite3 database.db < schema.sql

# Run the application
flask run
```

The app will be available at `http://127.0.0.1:5000`.

## Project structure

```
flashcards/
├── app.py              # Application entry point
├── db.py               # Database helpers
├── csrf.py             # CSRF protection
├── auth_utils.py       # Shared authentication helpers
├── schema.sql          # Database schema
├── routes/
│   ├── auth.py         # Registration, login, logout
│   ├── projects.py     # Project CRUD
│   ├── flashcards.py   # Flashcard CRUD
│   └── search.py       # Keyword search
├── repositories/
│   ├── users.py        # User database queries
│   ├── projects_repo.py # Project database queries
│   └── flashcards_repo.py # Flashcard database queries
├── templates/          # Jinja2 HTML templates
├── static/
│   └── style.css       # CSS
└── README.md
```

## How to test

1. Run `python3 seed.py` to populate the database with test data
2. Start the app with `flask run`
3. Log in as any seed user (e.g. `alice` / `password123`)
4. Open a project and browse flashcards — try the difficulty filter and pagination
5. Click "Study All Cards" to start a study session — answer cards and see the results
6. Click "Save and continue later" during a session, then use "Continue" to resume
7. Search for "bob" or "python" in the search bar to find users and public projects
8. Visit another user's public profile and view their public projects (read-only)
9. Click your username in the navbar to see your profile stats

## Testing with large data

The project includes `seed.py`, a script that populates the database with test data:
5 users, 10 projects, and 500+ flashcards with varied difficulty tags, plus study
session history.

```bash
python3 seed.py
```

This resets the database and creates fresh test data. All seed users have the
password `password123`.

The app handles large datasets well:

- **Pagination** keeps the project page fast — only 20 cards are loaded per page,
  even for projects with hundreds of flashcards
- **Difficulty filtering** combined with pagination uses `LIMIT`/`OFFSET` queries
  so only the needed rows are fetched
- **Database indexes** on key columns improve query performance:
  - `idx_projects_user_id` — fast lookup of a user's projects
  - `idx_flashcards_project` — fast lookup of a project's flashcards
  - `idx_flashcards_front` — speeds up text search on flashcard fronts
  - `idx_sessions_user` and `idx_sessions_project` — fast session lookups
  - `idx_session_answers_session` and `idx_session_cards_session` — fast session detail queries

## Code quality

Pylint was used to check code quality. The full report is in `pylint-report.md`.

```bash
pip install pylint
pylint app.py db.py csrf.py auth_utils.py seed.py routes/*.py repositories/*.py
```

Current score: **8.60 / 10**. Remaining warnings are mostly missing docstrings on
short, self-documenting functions and modules.

## Tech stack

- Backend; Python, Flask
- Database; SQLite (raw SQL, no ORM)
- Frontend; HTML + CSS
