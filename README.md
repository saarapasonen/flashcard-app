# Flashcards

A web application for creating and studying flashcards, built with Python and Flask.

## Features

- User registration and login
- Create, edit, and delete projects (collections of flashcards)
- Create, edit, and delete flashcards within projects
- Search flashcards by keyword across all projects

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
