from app import *
import random
import copy
import pytest

with app.app_context():

    test_meetings = []

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

    def return_random_group():
        with app.app_context():
            employee_list = []
            for person in employee.query:
                if random.random() > 0.5:
                    employee_list.append(person)
            test_group = group("testgroup",employee_list)
        return test_group

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
            test_meeting = meeting.query.get(0)
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

    @pytest.mark.parametrize('input',[0,'b',"garbage_string",[(1),(3),(6),(10)]])
    def test_room_conflicts_garbage(input):
        with app.app_context():
            assert find_room_conflict(input) == -1

    @pytest.mark.parametrize('test_number',[0,1])
    def test_romm_conflicts_no_conflict(test_number):
        with app.app_context():
            test_meeting = meeting.query.get(0)
            new_meeting = copy.deepcopy(test_meeting)
            if test_number == 0:
                new_meeting.Start -= timedelta(minutes = 10)
                new_meeting.End    = test_meeting.Start - timedelta(minutes = 5)
            elif test_number == 1:
                new_meeting.Start  = test_meeting.End + timedelta(minutes = 5)
                new_meeting.End   += timedelta(minutes = 10)
            assert find_room_conflict(new_meeting) == -1

    @pytest.mark.parametrize("input1,input2,expected",[
                # test 1 (starts too early)
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 7, 0, 0, 0),
                End = datetime(2024, 4, 20, 8, 0, 0, 0),
                Room_number = room.query.get(random.randrange(1,room.query.count(),1)),
                People = return_random_group(),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),
                employee(name='Jim',     employee_id = '1',  age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),1),
                
                # test 2 (valid time)
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 9, 0, 0, 0),
                End = datetime(2024, 4, 20, 10, 0, 0, 0),
                Room_number = room.query.get(random.randrange(1,room.query.count(),1)),
                People = return_random_group(),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),
                employee(name='Jim',     employee_id = '1',  age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),0),

                # test 3 (too late intersect with end time)
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 18, 0, 0, 0),
                End = datetime(2024, 4, 20, 19, 0, 0, 0),
                Room_number = room.query.get(random.randrange(1,room.query.count(),1)),
                People = return_random_group(),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),
                employee(name='Jim',     employee_id = '1',  age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),1),

                # test 4 (too late)
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 19, 0, 0, 0),
                End = datetime(2024, 4, 20, 20, 0, 0, 0),
                Room_number = room.query.get(random.randrange(1,room.query.count(),1)),
                People = return_random_group(),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),
                employee(name='Jim',     employee_id = '1',  age=26, start_work = time(7,30,0,0), end_work= time(18,30,0,0), Password = 123),1),
                
                # test 5 (invalid inputs)
                (0,1,-1)
                ])            
    def test_find_working_hours_conflict(input1,input2,expected):
        with app.app_context():
            assert find_working_hours_conflict(input1,input2) == expected

    @pytest.mark.parametrize("input,expected", [
                
                # test 1 no conflicts 
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 21, 12, 0, 0, 0),
                End = datetime(2024, 4, 21, 13, 0, 0, 0),
                Room_number = str(room.query.get(2).Room_number) + " " + room.query.get(2).Building,
                People = group("testgroup",[employee.query.get(4),employee.query.get(5),employee.query.get(6)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),0),

                # test 2 no employee time conflict, no room conflict, employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 12, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(2).Room_number) + " " + room.query.get(2).Building,
                People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),2),

                # test 3 no employee time conflict, room conflict, no employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 12, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(1).Room_number) + " " + room.query.get(1).Building,
                People = group("testgroup",[employee.query.get(4),employee.query.get(5),employee.query.get(6)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),1),
                
                # test 4 no employee time conflict, room conflict, employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 12, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(1).Room_number) + " " + room.query.get(1).Building,
                People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),1),

                 # test 5 employee time conflict, no room conflict, no employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 6, 0, 0, 0),
                End = datetime(2024, 4, 20, 8, 0, 0, 0),
                Room_number = str(room.query.get(2).Room_number) + " " + room.query.get(2).Building,
                People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),3),

                # test 6 no employee time conflict, no room conflict, employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 6, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(2).Room_number) + " " + room.query.get(2).Building,
                People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),2),

                # test 7  employee time conflict, room conflict, no employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 6, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(1).Room_number) + " " + room.query.get(1).Building,
                People = group("testgroup",[employee.query.get(4),employee.query.get(5),employee.query.get(6)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),1),

                # test 8  employee time conflict, room conflict, employee conflict
                (meeting( Meeting_id = meeting.query.count()+1,
                Start = datetime(2024, 4, 20, 6, 0, 0, 0),
                End = datetime(2024, 4, 20, 13, 0, 0, 0),
                Room_number = str(room.query.get(1).Room_number) + " " + room.query.get(1).Building,
                People = group("testgroup",[employee.query.get(1),employee.query.get(2),employee.query.get(3)]),
                Description = "Test_meeting: " + str(meeting.query.count()+1)),1),
                ])
    
    def test_find_universal_conflict(input,expected):
        with app.app_context():
            assert find_universal_time_conflict(input) == expected
