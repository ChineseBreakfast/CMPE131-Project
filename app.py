import re
import json
from datetime import time
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class employee(db.Model):
    name = db.Column(db.String(100), nullable = False)
    employee_id = db.Column(db.String(100), primary_key = True)
    age = db.Column(db.Integer, nullable = False)
    start_work = db.Column(db.types.Time())
    end_work = db.Column(db.types.Time())
    Password = db.Column(db.String(100),nullable = True)

class meeting(db.Model):
    Meeting_id = db.Column(db.Integer, primary_key = True)
    Start = db.Column(db.types.Time(), nullable = False)
    End = db.Column(db.types.Time(), nullable = False)
    Room_number = db.Column(db.String(10), nullable = False)
    People = db.Column(db.PickleType, nullable = False)

class room(db.Model):
    Room_number = db.Column(db.Integer, primary_key = True)
    meetings = db.Column(db.PickleType, nullable = True)

class group():
    group_name = ""
    employees = []
    def __init__ (self,group_name,employees):
        self.group_name = group_name
        self.employees = employees

class groupdb(db.Model):
    Group_ID = db.Column(db.Integer, primary_key = True)
    People = db.Column(db.PickleType, nullable = False)

@app.before_request
def create_and_populate_db():
    db.create_all()
    if employee.query.count == 0:
        employees = [                
            employee(name='Jim',  id = '1', age=26, start_work = time(8,30,0,0), end_work= time(18,30,0,0), Password = 123),
            employee(name='Jane', id = '2', age=53, start_work = time(7,30,0,0),end_work= time(18,30,0,0), Password = 456),
            employee(name='John', id = '3', age=34, start_work = time(8,0,0,0), end_work= time(18,30,0,0),Password = 789)
                    ]
        db.session.bulk_save_objects(employees)
        db.session.commit()

@app.route("/")    
def home():
    return render_template('index.html')

@app.route('/datainput1', methods = ["GET","POST"])
def data_submit():
    if request.method == "POST":
        names = request.form.getlist("select")
        start = request.form.get("Start")
        start = start.split(':')
        end = request.form.get("End")
        end = end.split(':')
        room_number = request.form.get("Room_number")
        new_meeting = meeting(Meeting_id = meeting.query.count()+1, Start = time(int(start[0]),int(start[1]),0,0), End = time(int(end[0]),int(end[1]),0,0), Room_number= room_number, People = names)
        db.session.add(new_meeting)
        db.session.commit()
    return render_template('input.html')

@app.route('/datainput2', methods = ["GET","POST"])
def data_submit2():
    if request.method == "POST": 
        employee_names = []
        name = request.form.get("name")
        password = request.form.get("password")
        age = request.form.get("age")
        start_work = request.form.get("start_work")
        start_work = start_work.split(':')
        end_work = request.form.get("end_work")
        end_work = end_work.split(':')
        new_employee = employee(name=name,  employee_id = employee.query.count()+1, age=age, start_work = time(int(start_work[0]),int(start_work[1]),0,0), end_work= time(int(end_work[0]),int(end_work[1]),0,0), Password = password)
        db.session.add(new_employee)
        db.session.commit()
    for i in range(employee.query.count()):
        info = employee.query.get(i+1)
        employee_names.append(info.name)
    return render_template('input.html', info=employee_names)
         
@app.route('/login', methods = ["GET","POST"])
def hello_there():
    employee_names = []
    if request.method == "POST":
        if (employee.query.count() == 0):
            employees = [                
            employee(name='Jim',  employee_id = '1', age=26, start_work = time(8,30,0,0), end_work= time(18,30,0,0), Password = 123),
            employee(name='Jane', employee_id = '2', age=53, start_work = time(7,30,0,0),end_work= time(18,30,0,0), Password = 456),
            employee(name='John', employee_id = '3', age=34, start_work = time(8,0,0,0), end_work= time(18,30,0,0),Password = 789)
                        ]
            db.session.bulk_save_objects(employees)
            db.session.commit()
        group1 = group("group1", [employee.query.get(1),employee.query.get(2),employee.query.get(3)])
        if (meeting.query.count() == 0):
            meetings = [
            meeting(Meeting_id = 1,Start = time(8,30,0,0) , End = time(11,30,0,0) ,Room_number = 1, People = group1),
            meeting(Meeting_id = 2,Start = time(11,50,0,0) , End = time(12,30,0,0) ,Room_number = 2, People = group1)
                    ]
            db.session.bulk_save_objects(meetings)
            db.session.commit()
        username = request.form.get("username")
        password = request.form.get("password")
        employee_num = employee.query.count()
        print(employee.query.count())
        for i in range(employee.query.count()):
            info = employee.query.get(i+1)
            if (info.name == username) and (info.Password == password):
                for i in range(employee.query.count()):
                    info = employee.query.get(i+1)
                    employee_names.append(info.name)
                return render_template('input.html', info=employee_names)

    
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
