from crypt import methods
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint("blog",__name__)

bp.route("/")
def index():
    db = get_db()
    posts = db.execute("SELECT p.id, p.title, p.body, p.created, p.author_id, u.username FROM post AS p"
                " JOIN  user AS u ON u.id = p.author_id ORDER BY p.created DESC").fetchall
    return render_template(url_for("blog/index.html", posts=posts))

bp.route("/create", methods=("GET","POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",(title, body, g.user["author_id"]))
            db.commit()
            return redirect(url_for("blog/create"))
    return render_template("blog/create.html")