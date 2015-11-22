# brew install geos
# pip install shapely
# pip install tzwhere
# pip install geopy


from geopy import geocoders
from datetime import datetime
from tzwhere import tzwhere
from pytz import timezone

CITIES = ['Toronto', 'Glasgow','London','Amsterdam','Brussels','Paris','Porto','Madrid','Barcelona','Berlin','Copenhagen','Tromso','Tallinn','Helsinki','Moscow','Kiev','Vilnius','Stockholm','Warsaw','Dubrovnik','Belgrade','Sarajevo','Milan','Rome','Budapest','Bucharest','Sofia','Istanbul','Antalya','Izmir','Baku','Ankara','Johannesburg','Rio de Janeiro','Sao Paulo','Buenos Aires','Melbourne','Singapore','Jakarta','Manila','Shanghai', 'Tokyo', 'Mexico City','Los Angeles','Seattle','Chicago','Nashville','New York','Montreal']
START_DATE = datetime.strptime("28/07/15", "%d/%m/%y")

g = geocoders.GoogleV3()
tz = tzwhere.tzwhere(shapely=False, forceTZ=False)

timezones = {}
for city in CITIES:
    place, (lat, lng) = g.geocode(city)
    tz_name = tz.tzNameAt(lat, lng)
    try:
        offset = timezone(tz_name).localize(datetime(2015,1,1)).strftime('%z')
    except:
        offset = 'unknown'
    if offset not in timezones:
        timezones[offset] = []
    timezones[offset].append(city)

for tz in sorted(timezones.keys()):
    print tz
    print timezones[tz]
