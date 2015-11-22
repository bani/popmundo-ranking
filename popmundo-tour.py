from datetime import datetime, timedelta

CITIES = ['Tokyo', 'Shanghai', 'Manila', 'Singapore', 'Jakarta', '*no show*', 'Melbourne',
'*no show*', 'Baku', 'Moscow', 'Tallinn', 'Helsinki', 'Vilnius', 'Kiev', 
'Bucharest', 'Ankara', 'Antalya', 'Istanbul', 'Izmir', 'Sofia',
'Belgrade', 'Dubrovnik', 'Sarajevo', 'Budapest', 'Warsaw', 'Copenhagen',
'Stockholm', 'Tromso', 'Berlin', 'Milan', 'Rome', 'Barcelona',
'Paris', 'Brussels', 'Amsterdam', 'Glasgow', 'London', 'Madrid',
'Porto', '*no show*', 'Johannesburg', 'Rio de Janeiro', 'Sao Paulo', 'Buenos Aires', '*no show*', 'Mexico City',
'New York', 'Montreal', 'Toronto',  'Chicago', 'Nashville', '*no show*', 'Seattle', 'Los Angeles']

YEAR_BEGIN = datetime.strptime("13/01/16", "%d/%m/%y")
BIG_BANG = 9
DEAD = 28
KOBE = 40
VACATION = [BIG_BANG, DEAD]
INTERVAL = [-2, -1, 0, 54, 55, 56, 110, 111, 112]

START_DATE = datetime.strptime("16/02/16", "%d/%m/%y")

no_show = []
for day in VACATION:
    for delta in INTERVAL:
        no_show.append(YEAR_BEGIN + timedelta(days=day + delta))

shows12 = []
shows22 = []

current_date = START_DATE

for i in xrange(0,len(CITIES),2):
    while current_date in no_show:
        shows12.append('*no show*')
        shows22.append('*no show*')
        current_date += timedelta(days=1)
    shows12.append(CITIES[i])
    shows22.append(CITIES[i+1])
    current_date += timedelta(days=1)

for s in shows12:
    print s

print "--------"

for s in shows22:
    print s
