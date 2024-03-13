import re
from datetime import datetime
from sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class employee(db.Model):
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    worktimes = db.Column(db.time, nullable=False)


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

engine.connect
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