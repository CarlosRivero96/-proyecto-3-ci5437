import sys
import json
from datetime import date, time

def calcVar(day,hour,local,visitor):
    if (visitor >= local):
        visitor -= 1
    return day*numOfHours*numOfParticipants*(numOfParticipants-1) + hour*numOfParticipants*(numOfParticipants-1) + local*(numOfParticipants-1) + visitor +1

with open(sys.argv[1], "r") as jsonFile:
    data = json.load(jsonFile)

#calculate number of days
start_date = date.fromisoformat(data["start_date"])
end_date = date.fromisoformat(data["end_date"])
numOfDays = (end_date - start_date).days +1

#calculate number of hours
start_time = time.fromisoformat(data["start_time"])
end_time = time.fromisoformat(data["end_time"])
numOfHours = (end_time.hour - start_time.hour)//2

numOfParticipants = len(data["participants"])

#cnfSAT = "p cnf %d %d\n" % (numOfDays*numOfHours*numOfParticipants*(numOfParticipants-1), numOfClausulas)
clausulas = set()
#no hay 2 partidos al mismo tiempo
for i in range(numOfDays):
    for j in range(numOfHours):
        vars = []
        for k in range(numOfParticipants):
            for l in range(numOfParticipants):
                if (l==k):
                    continue
                vars.append(calcVar(i,j,k,l))
        for a in range(len(vars)):
            for b in range(a+1,len(vars)):
                clausulas.add("-%d -%d 0\n" % (vars[a],vars[b]))
                print("-%d -%d 0" % (vars[a],vars[b]))
print()
#un equipo no juega dos partidos como visitante/local 2 dias consecutivos
for k in range(numOfParticipants):
    for i in range(numOfDays-1):
        dayL = []
        nextDayL = []
        dayV = []
        nextDayV = []
        for j in range(numOfHours):
            for l in range(numOfParticipants):
                if (l==k):
                    continue
                dayL.append(calcVar(i,j,k,l))
                nextDayL.append(calcVar(i+1,j,k,l))
                dayV.append(calcVar(i,j,l,k))
                nextDayV.append(calcVar(i+1,j,l,k))
        
        for a in dayL:
            for b in nextDayL:
                clausulas.add("-%d -%d 0\n" % (a,b))
                print("-%d -%d 0" % (a,b))
        for a in dayV:
            for b in nextDayV:
                clausulas.add("-%d -%d 0\n" % (a,b))
                print("-%d -%d 0" % (a,b))
print()

cnfSAT = ""
for a in clausulas:
    cnfSAT += a

# print(cnfSAT)

# data["participants"]