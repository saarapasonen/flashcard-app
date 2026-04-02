from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import check_password_hash
from csrf import validate_csrf
from repositories import users

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@validate_csrf
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("auth/register.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("auth/register.html")

        if users.find_by_username(username):
            flash("Username already taken.", "error")
            return render_template("auth/register.html")

        users.create(username, password)
        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@validate_csrf
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = users.find_by_username(username)

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Logged in.", "success")
            return redirect(url_for("projects.list_projects"))

        flash("Invalid username or password.", "error")
        return render_template("auth/login.html")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("auth.login"))
