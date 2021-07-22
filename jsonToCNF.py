import sys
import json
from datetime import date, time

def calcVar(day,hour,home,away):
    if (away >= home):
        away -= 1
    return day*numOfHours*numOfParticipants*(numOfParticipants-1) + hour*numOfParticipants*(numOfParticipants-1) + home*(numOfParticipants-1) + away +1

with open(sys.argv[1], "r") as jsonFile:
    data = json.load(jsonFile)

# calculate number of days
start_date = date.fromisoformat(data["start_date"])
end_date = date.fromisoformat(data["end_date"])
numOfDays = (end_date - start_date).days +1

# calculate number of hours
start_time = time.fromisoformat(data["start_time"])
end_time = time.fromisoformat(data["end_time"])
numOfHours = (end_time.hour - start_time.hour - (start_time.minute != 0 or start_time.second != 0))//2

numOfParticipants = len(data["participants"])

clausulas = set()

# there is no two matches at the same time
for i in range(numOfDays):
    for j in range(numOfHours):
        vars = []
        for k in range(numOfParticipants):
            for l in range(numOfParticipants):
                if (l==k):
                    continue
                vars.append(calcVar(i,j,k,l))
        vars.sort()
        for a in range(len(vars)):
            for b in range(a+1,len(vars)):
                clausulas.add("-%d -%d 0\n" % (vars[a],vars[b]))

# a team doesn't play two matches as local/away two days in a row
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
                clausulas.add("-%d -%d 0\n" % (min(a,b),max(a,b)))
        for a in dayV:
            for b in nextDayV:
                clausulas.add("-%d -%d 0\n" % (min(a,b),max(a,b)))

# a team plays at most once per day
for k in range(numOfParticipants):
    for i in range(numOfDays):
        games = []
        for j in range(numOfHours):
            for l in range(numOfParticipants):
                if (l==k):
                    continue
                games.append(calcVar(i,j,k,l))
                games.append(calcVar(i,j,l,k))
        
        games.sort()
        for a in range(len(games)):
            for b in range(a+1,len(games)):
                clausulas.add("-%d -%d 0\n" % (games[a],games[b]))

# a team must play against every other team exactly once as local and once as away
for k in range(numOfParticipants):
    for l in range(numOfParticipants):
        if (l==k):
            continue
        home = []
        for i in range(numOfDays):
            for j in range(numOfHours):
                home.append(calcVar(i,j,k,l))
        home.sort()
        # at least one
        clausulas.add(" ".join(str(x) for x in home) + " 0\n")
        # at most one
        for a in range(len(home)):
            for b in range(a+1,len(home)):
                clausulas.add("-%d -%d 0\n" % (home[a],home[b]))

print("p cnf %d %d\n" % (numOfDays*numOfHours*numOfParticipants*(numOfParticipants-1), len(clausulas)))

for a in clausulas:
    print(a,end="")
