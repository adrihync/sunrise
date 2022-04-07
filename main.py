from geopy.geocoders import Nominatim
import time
import datetime
from pprint import pprint
from suntime import Sun
import ephem
import math

app = Nominatim(user_agent="tutorial")

location = app.geocode("keswick, UK").raw

pprint(location)
print()

k_lat = location["lat"] 
k_lon = location["lon"]
k_elev = 90

print("lat:", k_lon, "long:",k_lat, "elevation:", k_elev)

sun = Sun(float(k_lat), float(k_lon))
k_rise = sun.get_local_sunrise_time()
#print("rise", k_rise, '\n')

obs = ephem.Observer()
obs.lat, obs.long, obs.elevation = k_lat, k_lon, k_elev
e_sun = ephem.Sun()
e_sunrise = obs.previous_rising(e_sun, start=ephem.now())
e_noon = obs.next_transit(e_sun, start=e_sunrise)
e_sunset = obs.next_setting(e_sun, start=e_noon)

print("e_rise", e_sunrise)
print("e_noon", e_noon)
print("e_set", e_sunset)

y_rise = obs.previous_rising(e_sun, start=e_sunrise)
y_noon = obs.previous_transit(e_sun, start=e_sunrise)
y_set = obs.previous_setting(e_sun, start=e_sunrise)

'''
print("y rise", y_rise)
print("y noon", y_noon)
print("y set", y_set)
'''
e_length = e_sunset-e_sunrise
#print(datetime.timedelta(days=e_length))
y_length = y_set - y_rise


print("day length today", datetime.timedelta(seconds=datetime.timedelta(days=y_length).seconds))

'''
print("day length yesterday", type(e_noon))
print(datetime.timedelta(seconds=datetime.timedelta(days=abs(e_length-y_length)).seconds))
'''
#yy_rise = datetime.datetime(y_rise)
c_length = abs(e_length - y_length)
c_str = "today " + ("longer" if e_length >= y_length else "shorter") + " than yesterday by " + str(datetime.timedelta(days=c_length))
print(c_str)

obs.date = e_noon
#pprint(obs)
s = ephem.Sun(obs)
print('Noon altitude: {:.1f} degrees'.format(s.alt / math.pi * 180.0))
