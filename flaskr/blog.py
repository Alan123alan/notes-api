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