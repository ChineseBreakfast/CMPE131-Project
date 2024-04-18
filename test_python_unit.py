from app import *
import random
import copy
import pytest
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
        
# we will create  examples of meetings that will have the same time and conflict with each other
# this only works for testing 1 meeting at a time
#  for each of those cases we will create times 
# fail     start1 < start2 & end 1 > end 2
# fail     start1 < start2 & end 1 < end 2 & end 1 > start 2
# succeed  start1 < start2 & end 1 < start 2
# fail     start1 > start2 & end 1 < end 2 & end 1 > start 2
# fail     start1 > start2 & end 1 > end 2
# succeed  start1 > end2   & end1 > end2  

@pytest.mark.parametrize('test_number',[0,1,2,3])
def test_room_conflicts_conflict(test_number):
    with app.app_context():
        for test_meeting in meeting.query:
                new_meeting = copy.deepcopy(test_meeting)
                if test_number == 0:
                    new_meeting.Start =  new_meeting.Start - timedelta(minutes = 5)
                    new_meeting.End   += timedelta(minutes = 5)
                elif test_number == 1:
                    new_meeting.Start -= timedelta(minutes = 5)
                    new_meeting.End   -= timedelta(minutes = 5)
                elif test_number == 2:
                    new_meeting.Start += timedelta(minutes = 5)
                    new_meeting.End   -= timedelta(minutes = 5)
                elif test_number == 3:
                    new_meeting.Start += timedelta(minutes = 5)
                    new_meeting.End   += timedelta(minutes = 5)
                assert find_room_conflict(new_meeting)[0]== new_meeting.Room_number

@pytest.mark.parametrize('test_number',[0,1])
def test_romm_conflicts_no_conflict(test_number):
    with app.app_context():
        for test_meeting in meeting.query:
            new_meeting = copy.deepcopy(test_meeting)
            if test_number == 0:
                new_meeting.Start -= timedelta(minutes = 10)
                new_meeting.End    = test_meeting.Start - timedelta(minutes = 5)
            elif test_number == 1:
                new_meeting.Start  = test_meeting.End + timedelta(minutes = 5)
                new_meeting.End   += timedelta(minutes = 10)
            assert find_room_conflict(new_meeting) == -1


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

