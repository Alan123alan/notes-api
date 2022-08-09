#from crypt import methods
#from crypt import methods
from os import abort
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .auth import login_required

bp = Blueprint("blog",__name__)

bp.route("/", methods=("GET",))
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


def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        "SELECT p.id, p.title, p.body, p.created, p.author_id ,u.username"
        "FROM post p JOIN user u ON u.id = p.author_id WHERE p.id = ?",
        (id,)
    ).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn´t exist.")
    if check_author and post["author_id"] != g.user["id"]:
        abort(403)
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))