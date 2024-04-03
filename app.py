import re
import json
from datetime import time, datetime, timedelta
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
    Start = db.Column(db.types.DateTime(), nullable = False)
    End = db.Column(db.types.DateTime(), nullable = False)
    Room_number = db.Column(db.String(100), nullable = False)
    People = db.Column(db.PickleType, nullable = False)
    Description = db.Column(db.String(100),nullable = True)

class room(db.Model):
    Room_ID = db.Column(db.Integer, primary_key = True)
    Room_number = db.Column(db.Integer, nullable = False)
    Building = db.Column(db.String(100),nullable = True)
    

class group():
    group_name = ""
    employees = []
    def __init__ (self,group_name,employees):
        self.group_name = group_name
        self.employees = employees

class groupdb(db.Model):
    Group_ID = db.Column(db.Integer, primary_key = True)
    People = db.Column(db.PickleType, nullable = False)

@app.route("/")    
def home():
    return render_template('index.html')

# route for meeting form submit
@app.route('/input_meeting', methods = ["GET","POST"])
def data_submit1():
    if request.method == "POST":
        # we initialize all of the data we get from the request form subission
        names = request.form.getlist("select")
        start = request.form.get("Start")
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(request.form.get("End"))
        room_number = request.form.get("Room_select")
        meeting_description = request.form.get("Meeting_description")

        # Create a new object with the data from the form submission, then commit it to the database
        new_meeting = meeting(Meeting_id = meeting.query.count()+1, Start = start, End = end, Room_number = room_number, People = names, Description = meeting_description)
        
        # Finds room conflicting times and creates an array of rooms that will not have a time conflict 
        room_conflict_bool = 0 
        Room_conflict_list = list(find_room_conflict(new_meeting))
        new_room_list = return_room_name_list()
        for i in Room_conflict_list:
            for j in new_room_list:
                if(i == j):
                    new_room_list.remove(j)
                    room_conflict_bool = 1
        if room_conflict_bool == 1 and room_number == "-1":
        # Will reload the page with only the rooms avaliable for that time, maybe there is a better way to do this without reloading the page
            return render_template('input.html', rooms = new_room_list, info = return_employee_name_list())
        else:
        
            if room_number == "-1": # If the user left the field blank, then the program will assign them a Room from the valid room list
                room_number = new_room_list[1]
            db.session.add(new_meeting)
            db.session.commit()
    return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list())

# route from employee form submit
@app.route('/input_employee', methods = ["GET","POST"])
def data_submit2():
    if request.method == "POST": 
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
    return render_template('input.html', rooms = return_room_name_list(), info=return_employee_name_list())
         
# route from room form submit
@app.route('/input_Room', methods = ["GET","POST"])
def data_submit3():
    if request.method == "POST": 
        found = 0 
        Room_number = request.form.get("Room Number")
        Building = request.form.get("Building")
        new_room = room(Room_number = Room_number, Building = Building)
        for i in range(room.query.count()):
            temp_room = room.query.get(i+1)
            if temp_room.Room_number == int(Room_number):
                found = 1
                break
        if found == 0 :
            new_room = room(Room_number = Room_number, Building = Building)
            db.session.add(new_room)
            db.session.commit()
    return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list())
      

@app.route('/login', methods = ["GET","POST"])
def hello_there():
    populate_database()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        employee_num = employee.query.count()
        print(employee.query.count())
        for i in range(employee.query.count()):
            info = employee.query.get(i+1)
            if (info.name == username) and (info.Password == password):
                return render_template('input.html', rooms = return_room_name_list(), info=return_employee_name_list())

@app.route('/get_valid_rooms', methods = ["PATCH"])
def return_valid_rooms():
    value = 1
    return
    
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)


def populate_database():
    db.create_all()
    
    if  employee.query.count() == 0:
        employees = [                
        employee(name='Jim',  employee_id = '1', age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),
        employee(name='Jane', employee_id = '2', age=53, start_work = time(7,30,0,0),end_work= time(18,30,0,0), Password = 456),
        employee(name='John', employee_id = '3', age=34, start_work = time(8,0,0,0), end_work= time(18,30,0,0),Password = 789) ]
        db.session.bulk_save_objects(employees)
        db.session.commit()
    group1 = group("group1", [employee.query.get(1),employee.query.get(2),employee.query.get(3)])    
    if (meeting.query.count() == 0):
        meetings = [
        meeting(Meeting_id = 1,Start = datetime.now()+ timedelta(hours = 2)          , End = datetime.now() + timedelta(hours = 5)           , Room_number = "324 Clark building"      , People = group1, Description = "Meeting 1"),
        meeting(Meeting_id = 2,Start = datetime.now()+ timedelta(days =2, hours = 4) , End = datetime.now() + timedelta(days = 2, hours = 7) , Room_number = "110 Engineering building", People = group1, Description = "Meeting 2") ]
        db.session.bulk_save_objects(meetings)
        db.session.commit()
    if room.query.count() == 0:
        defaultrooms = [
        room(Room_ID = 1, Room_number = 324, Building = "Clark building"),
        room(Room_ID = 2, Room_number = 110, Building = "Engineering building"),
        room(Room_ID = 3, Room_number = 532, Building = "Parker building")]
        db.session.bulk_save_objects(defaultrooms)
        db.session.commit()

# finds conflicts in room scheduling, returns an array of which meetings are conflicting 
def find_room_conflict(new_meeting):
    Room_conflict_list = []
    for i in range(meeting.query.count()):
            old_meeting = meeting.query.get(i+1)
#            if (new_meeting.Room_number == old_meeting.Room_number):
            if  ((datetime.fromisoformat(str(new_meeting.End))   > datetime.fromisoformat(str(old_meeting.Start)) and 
                  datetime.fromisoformat(str(new_meeting.Start)) < datetime.fromisoformat(str(old_meeting.End))) or 
                 (datetime.fromisoformat(str(new_meeting.End))   < datetime.fromisoformat(str(old_meeting.Start)) and 
                  datetime.fromisoformat(str(new_meeting.Start)) > datetime.fromisoformat(str(old_meeting.End)))):                                                                
                 Room_conflict_list.append(old_meeting.Room_number)

    return set(Room_conflict_list)

# todo maybe, create another version of this that takes in a masking array that excludes an input array
def return_room_name_list():
    rooms = []
    tempitem = []
    for i in range(room.query.count()):
        info = room.query.get(i+1)
        tempitem = str(info.Room_number) + " " + info.Building
        rooms.append(tempitem)
    return rooms

def return_employee_name_list():
    employee_names = []
    for i in range(employee.query.count()):
        info = employee.query.get(i+1)
        employee_names.append(info.name)
    return employee_names