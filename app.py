import re
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
 #   People = db.Column(db.PickleType, nullable = True)

class meeting(db.Model):
    Meeting_id = db.Column(db.Integer, primary_key = True)
    Start = db.Column(db.types.Time(), nullable = False)
    End = db.Column(db.types.Time(), nullable = False)
    Room_number = db.Column(db.Integer, nullable = False)
    People = db.Column(db.PickleType, nullable = False)

class room(db.Model):
    Room_number = db.Column(db.Integer, primary_key = True)
    meetings = db.Column(db.PickleType, nullable = True)

class groupdb(db.Model):
    group_id = db.Column(db.Integer, primary_key = True)
    group_db = db.Column(db.PickleType, nullable = False)

class group():
    group_name = ""
    employees = []
    def __init__ (self,group_name,employees):
        self.group_name = group_name
        self.employees = employees

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


@app.route('/login', methods = ["GET","POST"])
def hello_there():
    if request.method == "POST":
        if (employee.query.count() == 0):
            employees = [                
            employee(name='Jim Davis',  employee_id = '1', age=26, start_work = time(8,30,0,0), end_work= time(18,30,0,0), Password = 123),
            employee(name='Jane Doe', employee_id = '2', age=53, start_work = time(7,30,0,0),end_work= time(18,30,0,0), Password = 456),
            employee(name='John Dorne', employee_id = '3', age=34, start_work = time(8,0,0,0), end_work= time(18,30,0,0),Password = 789)
                        ]
            db.session.bulk_save_objects(employees)
            db.session.commit()
        # group1 = group("group1", [employee.query.get(1),employee.query.get(2),employee.query.get(3)])
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
                return render_template('input.html')

@app.route('/meeting_input', methods = ["GET","POST"])
def main_menu():
    if request.method == "POST":
     #   Room_number = request.form.get("username")
    #    password = request.form.get("password")

        return render_template('input.html')
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
   
if __name__ == '__main__':
    app.run(debug=True)