import sys
import json
from datetime import date, timedelta, datetime
from ics import Calendar, Event

def varCalc(var):
    temp = 0
    day = (var-1)//(numOfHours*numOfParticipants*(numOfParticipants-1))
    temp += day*(numOfHours*numOfParticipants*(numOfParticipants-1))
    hour = (var - temp -1)//(numOfParticipants*(numOfParticipants-1))
    temp +=  hour*(numOfParticipants*(numOfParticipants-1))
    local = (var-temp-1)//(numOfParticipants-1)
    temp += local * (numOfParticipants-1)
    away = var - temp - 1
    if (away >= local):
        away +=1
    return day,hour,local, away

def fun(variable):
    if (variable in letters):
        return True
    else:
        return False

with open(sys.argv[1], "r") as jsonFile:
    data = json.load(jsonFile)

# calculate number of days
start_date = date.fromisoformat(data["start_date"])
end_date = date.fromisoformat(data["end_date"])
numOfDays = (end_date - start_date).days +1

# calculate number of hours
start_time = datetime.fromisoformat("2000-01-01 " + data["start_time"])
end_time = datetime.fromisoformat("2000-01-01 " + data["end_time"])

if start_time.minute != 0 or start_time.second != 0:
    start_time += timedelta(hours=1, minutes= - start_time.minute, seconds = - start_time.second)

numOfHours = (end_time.hour - start_time.hour)//2
numOfParticipants = len(data["participants"])

file = open("glucoseResult.txt","r")

content = file.read()

if (content[0]=="U"):
    print("UNSAT D:")
    exit(1)

events = [int(x) for x in content.split(" ")[:-1] if int(x) > 0]

def createEvent(event):
    day,hour,home,away = varCalc(event)
    local = data['participants'][home]
    visitor = data['participants'][away]
    
    date = str(start_date + timedelta(days=day))
    start = str((start_time + timedelta(hours=2*hour)).time())
    end = str((start_time + timedelta(hours=2*hour+2)).time())

    e = Event()
    e.name = f'{local} - {visitor}'
    e.begin = f'{date} {start}'
    e.end = f'{date} {end}'
    return e

c = Calendar()
for e in events: c.events.add(createEvent(e))

with open('tournament.ics', 'w') as my_file:
    my_file.writelines(c)

print("SAT :D")