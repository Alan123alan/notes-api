import sqlite3
import click
""" Special object that points to the Flask application handling the request. 
Since you used an application factory, there is no application object when writing the rest of your code."""
from flask import current_app
""" Special object that is unique for each request. 
Used to store data that might be accessed by multiple functions during the request. 
The connection is stored and reused """
from flask import g  
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # establishes a connection to the file pointed at by the DATABASE configuration key
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # return rows that behave like dicts. This allows accessing the columns by name.

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()