from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from distance import distance
from math import floor

now = datetime.now()

isoDatetimeFormat = '%Y-%m-%dT%H:%M:%SZ'

def requestLastEvents(howMany):
	baselink = "https://service.iris.edu/fdsnws/event/1/query"
	params = {
		"limit":str(howMany),
		"orderby":"time",
		"format":"geocsv",
		"start":str((now - relativedelta(years=2)).date()),
		"end":str(now.date())
	}
	return requests.get(baselink, params)

def requestNearestStations(lat, lon, eventTime):
	baselink = "https://service.iris.edu/fdsnws/station/1/query"
	params = {
		"lat":str(lat),
		"lon":str(lon),
		"maxradius":20,
		"startbefore":str((eventTime - relativedelta(minute=5)).date()),
		"endafter":str((eventTime + relativedelta(minute=5)).date()),
		"format":"geocsv"
	}
	return requests.get(baselink, params)

def requestSac(networkId, stationId, eventTime, distance):
	baselink = "http://service.iris.edu/fdsnws/dataselect/1/query"
	timeshift = floor(distance/6) # Speed of seismic waves is between 2 and 6 km/s
	params = {
		"format":"sac.zip",
		"start":str((eventTime - relativedelta(seconds=timeshift)).date()),
		"end":str((eventTime + relativedelta(seconds=300-timeshift)).date()),
		"net":networkId,
		"sta":stationId
	}
	return requests.get(baselink, params)

def requestMultipleSacs(stations, event):
	eventTime = datetime.strptime(event['Time'], isoDatetimeFormat)
	requests = []
	for i in range(len(stations)):
		requests.append(requestSac(
			stations[i]["Network"],
			stations[i]["Station"],
			eventTime,
			distance(float(stations[i]['Longitude']), float(stations[i]['Latitude']), float(event['Longitude']), float(event['Latitude']))
		))
	return requests