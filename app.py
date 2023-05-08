import os
import datetime
from dotenv import load_dotenv, find_dotenv
import jwt
from flask import Flask
from flask import jsonify
from flask import request
# from .db import init_app
# from . import auth # using "." or "flaskr" means the same when importing a module
# from . import blog

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")

print(__name__)
app = Flask(__name__)

@app.post("/login")
def login():
    token = jwt.encode(payload=request.json,key=SECRET_KEY)
    return {"token":token} 

@app.get("/notes")
def notes():
    notes = {
        "author" : "Alan",
        "created" : datetime.datetime.now(),
        "note" : "Some note."
    }
    return notes
