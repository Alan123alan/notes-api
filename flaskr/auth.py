#from crypt import methods
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
                # takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders
                # the database library will take care of escaping the values so you are not vulnerable to a SQL injection attack.
                db.execute("INSERT INTO user (username, password) VALUES (?,?)",(username, generate_password_hash(password))) # For security, passwords should never be stored in the database directly.
                db.commit()
            except IntegrityError: # an sqlite3.IntegrityError will occur if the username already exists
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
            # dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session.
            # The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests.
            session.clear
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request # registers a function that runs before the view function, no matter what URL is requested.
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE user_id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# this decorator returns a new view function that wraps the original view it’s applied to. The new function checks if a user is loaded and redirects to the login page otherwise. 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # when using a blueprint, the name of the blueprint is prepended to the name of the function,
            # so the endpoint for the login function you wrote above is 'auth.login' because you added it to the 'auth' blueprint.
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
