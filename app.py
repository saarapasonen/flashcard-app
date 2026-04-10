import secrets
from flask import Flask
from db import close_db, init_db, get_db
from csrf import generate_csrf_token
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.flashcards import flashcards_bp
from routes.search import search_bp
from routes.sessions import sessions_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Register teardown and blueprints
app.teardown_appcontext(close_db)
app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(flashcards_bp)
app.register_blueprint(search_bp)
app.register_blueprint(sessions_bp)

# Make csrf_token available in all templates
app.jinja_env.globals["csrf_token"] = generate_csrf_token

with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
