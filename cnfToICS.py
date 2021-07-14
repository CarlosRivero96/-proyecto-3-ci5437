import sys
import json
from datetime import date, time

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
    return [day,hour,local, away]

with open(sys.argv[1], "r") as jsonFile:
    data = json.load(jsonFile)

# calculate number of days
start_date = date.fromisoformat(data["start_date"])
end_date = date.fromisoformat(data["end_date"])
numOfDays = (end_date - start_date).days +1

# calculate number of hours
start_time = time.fromisoformat(data["start_time"])
end_time = time.fromisoformat(data["end_time"])
numOfHours = (end_time.hour - start_time.hour)//2

numOfParticipants = len(data["participants"])

file = open("glucoseResult.txt","r")