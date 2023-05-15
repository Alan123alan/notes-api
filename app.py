import os
import datetime
from tabnanny import check
from dotenv import load_dotenv, find_dotenv
from cryptography.hazmat.primitives import serialization
import jwt
from flask import Flask
from flask import jsonify
from flask import request
from models import *
from pony.orm import db_session
from pony.orm import select
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

PRIVATE_KEY = serialization.load_ssh_private_key(open("id_rsa", "r").read().encode(), password=b"") 
PUBLIC_KEY = serialization.load_ssh_public_key(open("id_rsa.pub", "r").read().encode())

#Loading secret key from .env file to environment variables then loading into app
# load_dotenv(find_dotenv())
# SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    # The db session decorator seems to not be needed since when applying 
    # @token_required to the endpoint function the @db_session will wrap it 
    # @db_session
    def decorator(*args, **kwargs):
        token = None
        data = None
        current_user = None
        if "x-access-tokens" in request.headers:
            token = request.headers.get("x-access-tokens")
        else:
            return {"message":"A valid token is missing."}
        try:
            data = jwt.decode(jwt=token, key=PUBLIC_KEY, algorithms=["RS256", ])
            current_user = select(user for user in User if user.public_id == data["public_id"])
            if current_user:
                return f(*args, **kwargs)
        except:
            return {"message":"Token is invalid.", "token":token, "data": data, "current_user":current_user}
    return decorator


def check_if_registered(username:str, password:str)->bool:
    pass


db.bind("sqlite", "app.db", create_db=True)
db.generate_mapping(create_tables=True)


app = Flask(__name__)


@app.post("/register")
@db_session
def register():
    #If you want to use the secret stored in the env variable SECRET_KEY
    #token = jwt.encode(payload=request.json,key=SECRET_KEY, algorithm="HSA256")
    payload = request.json
    hashed_password = generate_password_hash(payload["password"], method="sha256")
    user = User(public_id=str(uuid.uuid4()), name=payload["name"], password=hashed_password, is_admin=False)
    # token = jwt.encode(payload=request.json,key=PRIVATE_KEY, algorithm="RS256")
    return {"message":"Registered succesfully.", "user":user.__dict__()} 


@app.post("/login")
@db_session
def login():
    #If you want to use the secret stored in the env variable SECRET_KEY
    #token = jwt.encode(payload=request.json,key=SECRET_KEY, algorithm="HSA256")
    payload = request.json
    user = select(user for user in User if user.public_id == payload["public_id"])
    if user:
        token = jwt.encode(payload=payload,key=PRIVATE_KEY, algorithm="RS256")
        return {"token":token, "payload":payload}
    return {"message":"Invalid username or password"} 


@app.post("/notes")
@db_session
@token_required
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
