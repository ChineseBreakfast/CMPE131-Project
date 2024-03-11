import re
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/login', methods = ["GET","POST"])
def hello_there():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
    return 