import os
import datetime
from dotenv import load_dotenv, find_dotenv
from cryptography.hazmat.primitives import serialization
import jwt
from flask import Flask
from flask import jsonify
from flask import request
from models import *
from pony.orm import db_session
from pony.orm import select

PRIVATE_KEY = serialization.load_ssh_private_key(open("id_rsa", "r").read().encode(), password=b"") 

#Loading secret key from .env file to environment variables then loading into app
# load_dotenv(find_dotenv())
# SECRET_KEY = os.getenv("SECRET_KEY")


db.bind("sqlite", "app.db", create_db=True)
db.generate_mapping(create_tables=True)


app = Flask(__name__)



@app.post("/login")
def login():
    #If you want to use the secret stored in the env variable SECRET_KEY
    #token = jwt.encode(payload=request.json,key=SECRET_KEY, algorithm="HSA256")
    token = jwt.encode(payload=request.json,key=PRIVATE_KEY, algorithm="RS256")
    return {"token":token} 

@app.post("/notes")
@db_session
def post_notes():
    body = request.json
    author = Author(name=body["author"])
    note = Note(author=author, title=body["title"], body=body["body"])
    return note.__dict__()


@app.get("/notes")
@db_session
def get_notes():
    notes = [n.__dict__() for n in list(select(note for note in Note)[:])]
    print(notes)
    return notes


@app.get("/notes/<string:author_name>")
@db_session
def get_author_notes(author_name):
    notes = [n.__dict__() for n in list(select(note for note in Note if note.author.name == author_name)[:])]
    print(notes)
    return notes


@app.get("/notes/<int:id>")
@db_session
def get_note(id):
    notes = [n.__dict__() for n in list(select(n for n in Note if n.id == id)[:])]
    return notes


if(__name__ == "__main__"):
    app.run(debug=True)
