import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class employee(db.Model):
    name = db.Column(db.String(100), nullable = False)
    employee_id = db.Column(db.String(100), primary_key = True)
    age = db.Column(db.Integer, nullable = False)
    start_work = db.Column(db.TEXT, nullable = False)
    end_work = db.Column(db.TEXT, nullable = False)
    Password = db.Column(db.String(100),nullable = True)

class meetings(db.Model):
    Meeting_id = db.Column(db.Integer, primary_key = True)
    Start = db.Column(db.TEXT, nullable = False)
    End = db.Column(db.TEXT, nullable = False)
    Room_number = db.Column(db.Integer, nullable = False)
    People = db.Column(db.string, nullable = True)

class rooms(db.Model):
    Room_number = db.Column(db.integer, primary_key = True)
    meetings = db.Column(db.string,nullable = True)

@app.before_request
def create_and_populate_db():
    db.create_all()

    if employee.query.count() == 0:
        employee = [
            employee(name='Jim',  id = '1', age=26, start_work = datetime.time(8,30,0,0), end_work= datetime.time(18,30,0,0), password = 123),
            employee(name='Jane', id = '2', age=53, start_work = datetime.time(7,30,0,0),end_work= datetime.time(18,30,0,0), password = 456),
            employee(name='John', id = '3', age=34, start_work = datetime.time(8,0,0,0), end_work= datetime.time(18,30,0,0),password = 789)
                    ]
        db.session.bulk_save_objects(employee)
        db.session.commit()

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/login', methods = ["GET","POST"])
def hello_there():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        for i in employee.query.count():
            info = employee.query.get(i)
            if (info.username() == username) and (info.password() == password):
                return render_template('placeholder.html')

    
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
    return render_template('index.html')