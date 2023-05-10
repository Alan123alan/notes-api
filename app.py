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

# @app.get("/notes")
# def notes():
#     notes = [{
#         "author" : "Alan",
#         "created" : datetime.datetime.now(),
#         "note" : "Some note."
#     }]
#     return notes

@app.post("/notes")
@db_session
def post_notes():
    body = request.json
    note = Note(author=body["author"], title=body["title"], body=body["body"])
    return {"author":note.author}


if(__name__ == "__main__"):
    app.run(debug=True)
