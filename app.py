import re
import json
import pickle
import random
from datetime import time, datetime, timedelta, date
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, current_app, g 

debug = 1
NUMBER_OF_MEETINGS = 10



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


def setglobal(value):
    global global_meeting
    global_meeting = value

def setsave(value):
    global save_meeting
    save_meeting = value

@app.route("/")    
def home():
    populate_database()
    if debug:
            print_all_meetings()
    return render_template('index.html')

# route for meeting form submit
@app.route('/input_meeting', methods = ["GET","POST"])
def data_submit1():
    alert = [-1,"0"]

    # "GET" is used if an error is found and the user needs to change their meeting
    if request.method == "GET":
        answer = request.values.get('response')
        if (answer == '1'):
            db.session.add(global_meeting)
            db.session.commit()
        elif(answer == '2'):
            db.session.add(save_meeting)
            db.session.commit()
        setsave(meeting())
        setglobal(meeting())
            
    if request.method == "POST":

        # initialize the less complicated data
        start = datetime.fromisoformat(request.form.get("Start"))
        end = datetime.fromisoformat(request.form.get("End"))
        room_number = request.form.get("Room_select")
        meeting_description = request.form.get("Meeting_description")

        # check for errors in time inputs 
        delta =  end-start
        if delta < timedelta(seconds=0):
            error_message = (4,"Start time can not be after end time")
            return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = error_message)
        if delta > timedelta(hours = 8):
            error_message = (5,"Your meeting is too long, and will not be able to fit in any schedule, please consider breaking this into multiple meetings")
            return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = error_message)
        
        # we initialize the names from the form submission into employee objects that we can pass to the schedule checking function
        names = request.form.getlist("select")
        employee_names = employee.query
        names_object = group("",[])
        count = 0
        for i in employee_names:
            if ((count < len(names)) and (i.name == names[count])):
                names_object.employees.append(employee_names[count])
                count = count+1

        # Create a new object with the data from the form submission, then commit it to the database
        new_meeting = meeting(Meeting_id = meeting.query.count()+1, Start = start, End = end, Room_number = room_number, People = names_object, Description = meeting_description)
        
        # find any time conflicts with the new meeting
        conflict = find_universal_time_conflict(new_meeting)
        if conflict != 0:
            recommended_meeting = reccomend_new_meeting_times(new_meeting, [0,0,0])
            
            # we will use global variables to save our meeting objects during the context switch from python to javascript
            setsave(new_meeting)
            setglobal(recommended_meeting)
            
            # 1 if there is a room conflict
            if (conflict == 1):               
                alert[0] = 1
                alert[1] = "There is a room conflict at this time, would you like to reschedule the meeting for this start time: " + str(recommended_meeting.Start) + " ?"
                return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = alert)
            
            # 2 if there is an employee conflict with another meeting
            elif(conflict == 2):
                employee_conflict_list = find_meeting_conflicts(new_meeting)
                alert[0] = 2
                alert[1] = "The following employees have meetings at this time:"
                for employee_it in employee_conflict_list:
                    alert[1] = alert[1] + str(employee_it) + " "
                alert[1] = alert[1] + ", would you like to reschedule the meeting for this start time: "  + str(recommended_meeting.Start) + " ?"
                return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = alert)
            
            # 3 if there is an conflict with employee working hours 
            elif(conflict == 3):
                alert[0] = 3
                alert[1] = "There is a working hours conflict at this time, would you like to reschedule the meeting for this start time: " + str(recommended_meeting.Start) + " ?"
                return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = alert)
            # return 0 if there is no time conflict 
        else:
            db.session.add(new_meeting)
            db.session.commit()    
            
    return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = alert)

# route from employee form submit
@app.route('/input_employee', methods = ["GET","POST"])
def data_submit2():
    alert = -1
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
    return render_template('input.html', rooms = return_room_name_list(), info=return_employee_name_list(),alert = alert)
         
# route from room form submit
@app.route('/input_Room', methods = ["GET","POST"])
def data_submit3():
    alert = (-1,"0")
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
    return render_template('input.html', rooms = return_room_name_list(), info = return_employee_name_list(), alert = (3,alert))
      

@app.route('/login', methods = ["GET","POST"])
def hello_there():
    if request.method == "POST":
        return_meeting_times(datetime.now(), datetime.now()+timedelta(days= 1, hours = 2))
        username = request.form.get("username")
        password = request.form.get("password")
        employee_num = employee.query.count()
        print(employee.query.count())
        for i in range(employee.query.count()):
            info = employee.query.get(i+1)
            if (info.name == username) and (info.Password == password):
                return render_template('input.html', rooms = return_room_name_list(), info=return_employee_name_list(), alert=[-1,"1"])

@app.route('/get_valid_rooms', methods = ["PATCH"])
def return_valid_rooms():
    value = 1
    return
    
# todo; once the password is collected, we need to check 
# it against all of the other passwords in the database
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

def generate_random_meetings(number):
    random_meetings = []
    for meeting_number in range(0,number):
        # create an array of random employees to be added to each test meeting 
        employee_list = []
        for person in employee.query:
            if random.random() > 0.5:
                employee_list.append(person)
        test_group = group("testgroup",employee_list)       

        # create a random start time within the week, and the duration of the meeting 
        start_time_days = random.randrange(1,7,1)
        start_time_hours =  random.randrange(9,17,1)
        meeting_time = random.randrange(30,240,5)
        start_date = datetime(year = datetime.now().year, month=datetime.now().month,  day = datetime.now().day)
        end_date = datetime(year = datetime.now().year,month=datetime.now().month, day = datetime.now().day)
        start_date = start_date + timedelta(days = start_time_days,  hours = start_time_hours)
        end_date = end_date + timedelta(days = start_time_days,  hours = start_time_hours, minutes = meeting_time)
        
        # get a random room from the rooms avaliable
        test_room = room.query.get(random.randrange(1,room.query.count(),1))
        test_room = str(test_room.Room_number) +" "+ str(test_room.Building)
        new_meeting = meeting(Meeting_id = meeting_number, Start = start_date, End = end_date, Room_number = test_room, People = test_group, Description = "Test_meeting: " + str(meeting_number))
        db.session.add(reccomend_new_meeting_times(new_meeting,[0,0,0]))
        db.session.commit()
    return random_meetings
        
def populate_database():
    db.create_all()
    if  employee.query.count() == 0:
        employees = [                
        employee(name='Jim',     employee_id = '1',  age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),
        employee(name='Jane',    employee_id = '2',  age=53, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 456),
        employee(name='John',    employee_id = '3',  age=34, start_work = time(8,0,0,0),  end_work= time(18,30,0,0), Password = 789),
        employee(name='Emily',   employee_id = '4',  age=32, start_work = time(8,15,0,0), end_work= time(17,45,0,0), Password = 246),
        employee(name='David',   employee_id = '5',  age=45, start_work = time(8,30,0,0), end_work= time(18,0,0,0),  Password = 135),
        employee(name='Sarah',   employee_id = '6',  age=29, start_work = time(9,0,0,0),  end_work= time(17,30,0,0), Password = 579),
        employee(name='Michael', employee_id = '7',  age=38, start_work = time(7,45,0,0), end_work= time(17,15,0,0), Password = 802),
        employee(name='Laura',   employee_id = '8',  age=50, start_work = time(8,0,0,0),  end_work= time(18,30,0,0), Password = 951),
        employee(name='Chris',   employee_id = '9',  age=31, start_work = time(7,30,0,0), end_work= time(16,45,0,0), Password = 357),
        employee(name='Michelle',employee_id = '10', age=47, start_work = time(9,15,0,0), end_work= time(18,15,0,0), Password = 624) ]
        db.session.bulk_save_objects(employees)
        db.session.commit()
    group1 = group("group1", [employee.query.get(1),employee.query.get(2),employee.query.get(3)])    
    if room.query.count() == 0:
        defaultrooms = [
        room(Room_ID = 1,  Room_number = 324, Building = "Clark building"),
        room(Room_ID = 2,  Room_number = 110, Building = "Engineering building"),
        room(Room_ID = 3,  Room_number = 532, Building = "Parker building"),
        room(Room_ID = 4,  Room_number = 201, Building = "Smith Hall"),
        room(Room_ID = 5,  Room_number = 415, Building = "Johnson Center"),
        room(Room_ID = 6,  Room_number = 102, Building = "Wilson Library"),
        room(Room_ID = 7,  Room_number = 711, Building = "Taylor Hall"),
        room(Room_ID = 8,  Room_number = 604, Building = "Anderson Complex"),
        room(Room_ID = 9,  Room_number = 821, Building = "Brown Residence"),
        room(Room_ID = 10, Room_number = 318, Building = "Robinson Hall") ]
        db.session.bulk_save_objects(defaultrooms)
        db.session.commit()
    if (meeting.query.count() == 0):
        meetings = generate_random_meetings(NUMBER_OF_MEETINGS)

        # db.session.add(meeting(
        #     Meeting_id = meeting.query.count()+1,
        #     Start = datetime(2024, 4, 20, 12, 30, 0, 0),
        #     End = datetime(2024, 4, 20, 14, 0, 0, 0),
        #     Room_number = "324 Clark building",
        #     People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
        #     Description = "Test_meeting: " + str(meeting.query.count()+1)),2)
        # db.session.commit()
            

# return a list of employees objects who have time conflicts with the proposed meeting
def find_meeting_conflicts(new_meeting):
    employee_conflict_list = []
    # check for conflicts with other meetings
    for old_meeting in meeting.query:
        # this if statement checks if two meetings overlap 
        if  ((datetime.fromisoformat(str(new_meeting.End))   > datetime.fromisoformat(str(old_meeting.Start)) and 
              datetime.fromisoformat(str(new_meeting.Start)) < datetime.fromisoformat(str(old_meeting.End)))  or 
             (datetime.fromisoformat(str(new_meeting.End))   < datetime.fromisoformat(str(old_meeting.Start)) and 
              datetime.fromisoformat(str(new_meeting.Start)) > datetime.fromisoformat(str(old_meeting.End)))):
            # get an array of employees for each of the meetings we are compairing 
            employee_list = old_meeting.People.employees
            new_employee_list = new_meeting.People.employees
            # Compare the employee lists and find any duplicate names and ID's
            # If we find any duplicates we will add them ot the conflict list 
            for j in employee_list:
                for k in new_employee_list:
                    exists = False
                    if j.name == k.name and j.employee_id == k.employee_id:
                        # check if item already exists in the array 
                        for l in employee_conflict_list: 
                            if l.name == k.name and l.employee_id == k.employee_id:
                                exists = True
                        if exists == False:
                            employee_conflict_list.append(j)

                        # debug printout 
                        if (debug == 1):
                            print("there is A time conflict with employee:" + j.name)
                            print("The times:\n" + str(new_meeting.Start) +" to \n"+ str(new_meeting.End) + " conflicts with ")
                            print(str(old_meeting.Start) +" to \n"+ str(old_meeting.End))
    return employee_conflict_list # return the conflict list 

def reccomend_new_meeting_times(new_meeting,catchloop):
    # catchloop detects if the program cannot find a suitable meeting on the same day, so picks the next day to have the meeting 
    for i in catchloop:
        if i > 10:
            catchloop = [0,0,0]
            new_meeting.Start = new_meeting.Start + timedelta(days=1)
            new_meeting.End = new_meeting.End + timedelta(days=1)
    delta =  new_meeting.End - new_meeting.Start 
    scuffed_switch = find_universal_time_conflict(new_meeting)
    if scuffed_switch == 0:
        catchloop = [0,0,0]
        return new_meeting
    # room meeting conflict
    elif scuffed_switch == 1: 
        if debug:
            print("conflict 1: room and time conflict")
            print("New meeting Time" + str(new_meeting.Start))
        for room_it in room.query:
            if new_meeting.Room_number != str(room_it.Room_number) + " " + room_it.Building:
               new_meeting.Room_number  = str(room_it.Room_number) + " " + room_it.Building
               catchloop[2] = catchloop[2] + 1
               return reccomend_new_meeting_times(new_meeting,catchloop)
    # employee meeting conflict
    elif scuffed_switch == 2:
        if debug:
            print("conflict 2: Employee time conflict")
            print("New meeting Time" + str(new_meeting.Start))
        for  meeting_it in meeting.query:
            if find_time_conflict(meeting_it,new_meeting) == 1:
                new_meeting.Start = meeting_it.End + timedelta(minutes=10)
                new_meeting.End = new_meeting.Start + timedelta(seconds=delta.seconds)
                catchloop[0] = catchloop[0] + 1
                return reccomend_new_meeting_times(new_meeting,catchloop)
        
    # employee working hours conflict
    elif scuffed_switch == 3: 
        if debug:
            print("conflict 3: working hour conflict")
            print("New meeting Time" + str(new_meeting.Start))
        delta =  new_meeting.End - new_meeting.Start 
        min = datetime.now()
        for employee_it in new_meeting.People.employees:
            if min < datetime.combine(datetime(new_meeting.Start.year,new_meeting.Start.month,new_meeting.Start.day,0,0,0,0), employee_it.start_work):
                min = datetime.combine(datetime(new_meeting.Start.year,new_meeting.Start.month,new_meeting.Start.day,0,0,0,0), employee_it.start_work)
        new_meeting.Start = datetime(new_meeting.Start.year, new_meeting.Start.month, new_meeting.Start.day, min.hour, min.minute,0,0) + timedelta(minutes=10)
        new_meeting.End = new_meeting.Start + timedelta(seconds=delta.seconds)
        catchloop[1] = catchloop[1] + 1
        return reccomend_new_meeting_times(new_meeting,catchloop)


# return 0 if there is no time conflict
# return 1 if there is a room conflict
# return 2 if there is an employee conflict with another meeting
# return 3 if there is an conflict with employee working hours 
def find_universal_time_conflict(new_meeting):
    for  meeting_it in meeting.query:
        if find_time_conflict(meeting_it,new_meeting) == 1:
            if (meeting_it.Room_number == new_meeting.Room_number):
                    if debug:
                        print("The meeting at time" + str(meeting_it.Start) + " to " + str(meeting_it.End) + " Conflicts with " + str(new_meeting.Start) + " to " + str(new_meeting.End))
                    return 1
            for employee_it1 in meeting_it.People.employees:
                for employee_it2 in new_meeting.People.employees:
                    if (employee_it1.name == employee_it2.name) and (employee_it1.employee_id == employee_it2.employee_id):
                        return 2
    for  employee_it in new_meeting.People.employees:
        if find_working_hours_conflict(new_meeting,employee_it):
            return 3                
    return 0 
                
# check for conflicts with working time (i.e. if the employee does not work at those hours )
# given an input meeting and an input employee, it will find if there is a conflict
# if there is a conflict it will return 1, else it will return 0, -1 if invalid inputs
def find_working_hours_conflict(test_meeting,test_employee):
    if ((type(test_meeting) is meeting) and (type(test_employee) is employee)): 
        employee_start = datetime.combine(test_meeting.Start,test_employee.start_work)
        employee_end = datetime.combine(test_meeting.End,test_employee.end_work)
        if  (test_meeting.End  < employee_end) and (test_meeting.Start > employee_start):
            return 0
        else:
            return 1
    else: 
        return -1

# finds conflicts in room scheduling, returns an array of which meetings are conflicting 
def find_room_conflict(new_meeting):
    Room_conflict_list = []
    for  old_meeting in meeting.query:
        if(find_time_conflict(new_meeting,old_meeting) == -1):
            print("One of the meeting objects is invalid")
            return -1
        elif  (find_time_conflict(new_meeting,old_meeting)):
            Room_conflict_list.append(old_meeting.Room_number)
        
    if len(Room_conflict_list) == 0:
        return -1
    else:
        # remove duplicate items using set
        Room_conflict_list = set(Room_conflict_list)
        return list(Room_conflict_list)
    
# todo maybe, create another version of this that takes in a masking array that excludes an input array
def return_room_name_list():
    rooms = []
    tempitem = []
    for i in range(room.query.count()):
        info = room.query.get(i+1)
        tempitem = str(info.Room_number) + " " + info.Building
        rooms.append(tempitem)
    return rooms

# returns a list of all of the employees 
def return_employee_name_list():
    employee_names = []
    for i in range(employee.query.count()):
        info = employee.query.get(i+1)
        employee_names.append(info.name)
    return employee_names

# return a list of employee names given a meeting object
def return_meeting_participants(meeting):
    employee_names = []
    for i in meeting.People.employees:
        employee_names.append(i.name)
    return employee_names

# return a list of all of the meetings
def return_all_meeting_objects():
    return_meetings = []
    for i in meeting.query:
        return_meetings.append(i)
    return return_meetings

# return a list of all of the meetings
def return_all_meeting_Ids():
    return_meetings = []
    for i in meeting.query:
        return_meetings.append(i.Meeting_id)
    return return_meetings

# output is an array of meeting times, the input is 2 dates 
# on error returns -1 
# returns in the format starttime||endtime||roomnumber||description||# of employees attending||[List of employees]
def return_meeting_times(start_date,end_date):
    return_meeting_objects = []
    #check if the inputs are valid datetime objects 
    if((type(start_date) is datetime) and (type(end_date) is datetime)): 
        if (start_date > end_date):
            print("Invalid date range")
            return -1
        else:
            # itterate through all meetings
            for i in meeting.query:
                 # check if that meeting fits within the 2 dates provided 
                if ((i.Start > start_date) and (i.End < end_date)):
                    tempstring = str(i.Start) +"||"+ str(i.End)+"||"+i.Room_number+"||"+i.Description+"||"+str(len(i.People.employees))+"||"
                    # itterate through all employees registered for that meeting 
                    for j in i.People.employees: 
                        tempstring = tempstring + j.name +","
                    return_meeting_objects.append(tempstring)
            return return_meeting_objects
    else:
        print("invalid date time")
        return -1
    
# input two meetings and return 0 if there is no conflic and 1 if there is a conflict
# return -1 if there is a type error
def find_time_conflict(meeting1,meeting2):
    if ((type(meeting1) is meeting) and (type(meeting2) is meeting)): 
        if  ((datetime.fromisoformat(str(meeting1.End))   > datetime.fromisoformat(str(meeting2.Start)) and 
                datetime.fromisoformat(str(meeting1.Start)) < datetime.fromisoformat(str(meeting2.End)))  or 
            (datetime.fromisoformat(str(meeting1.End))   < datetime.fromisoformat(str(meeting2.Start)) and 
                datetime.fromisoformat(str(meeting1.Start)) > datetime.fromisoformat(str(meeting2.End)))):
            return 1
        else:
            return 0
    else: 
        return -1

def print_all_meetings():
    for meeting_it in meeting.query:
        print_meeting_data(meeting_it)

# print meeting data 
def print_meeting_data(meeting):
    print("Meeting ID: " + str(meeting.Meeting_id))
    print("Start Time: " + str(meeting.Start))
    print("End Time: " + str(meeting.End))
    print("Room: " + meeting.Room_number)
    print("Attendies:")
    for employee_it in meeting.People.employees:
        print(employee_it.name)
    print("Description: " + meeting.Description)