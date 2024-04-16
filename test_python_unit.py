from app import *
import random
def func(x):
    return x + 1


test_meetings = []

def test_return_meeting_participants():
    with app.app_context():
        for test_meeting in test_meetings:       
            names_list = []
            for i in test_meeting.People.employees:
                names_list.append(i.name)
            assert return_meeting_participants(test_meeting) == names_list

def test_return_employee_name_list():
    employee_names = []
    with app.app_context():
        for i in range(employee.query.count()):
            info = employee.query.get(i+1)
            employee_names.append(info.name)
        assert return_employee_name_list() == employee_names
        
# create an array of 10 meetings to test 
with app.app_context():
    for meeting_number in range(0,10):
        # create an array of random employees to be added to each test meeting 
        employee_list = []
        for person in employee.query:
            if random.random() > 0.5:
                employee_list.append(person)
        test_group = group("testgroup",employee_list)       

        # create a random start time within the week, and the duration of the meeting 
        start_time_days = random.randrange(1,5,1)
        start_time_hours =  random.randrange(9,17,1)
        meeting_time = random.randrange(0,240,5)
        test_room = room.query.get(random.randrange(1,room.query.count(),1))

        test_meetings.append(meeting( 
            Meeting_id = meeting.query.count()+1,
            Start = datetime.now()+ timedelta(days = start_time_days,  hours = start_time_hours),
            End = datetime.now() + timedelta(days = start_time_days,  hours = start_time_hours, minutes = meeting_time ),
            # get a random room from the rooms avaliable
            
            Room_number = test_room,
            People = test_group,
            Description = "Test_meeting: " + str(meeting.query.count()+1)))




