from crypt import methods
import functools
from sqlite3 import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")# The url_prefix will be prepended to all the URLs associated with the blueprint.

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        
        if error is None:
            try:
                """ takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders
                the database library will take care of escaping the values so you are not vulnerable to a SQL injection attack."""
                db.execute("INSERT INTO user (username, password) VALUES (?,?)",(username, generate_password_hash(password))) # For security, passwords should never be stored in the database directly.
                db.commit()
            except db.IntegrityError: # an sqlite3.IntegrityError will occur if the username already exists
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods=("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = f"User {username} doesn´t exist."
        elif not check_password_hash(user["password"],password):
            error = "Incorrect password."
        
        if error is None:
            session.clear
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

