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
		"maxradius":5,
		"startbefore":datetime.strftime((eventTime - relativedelta(minute=5)), isoDatetimeFormat),
		"endafter":datetime.strftime((eventTime + relativedelta(minute=5)), isoDatetimeFormat),
		"format":"geocsv"
	}
	return requests.get(baselink, params)

def requestSac(networkId, stationId, eventTime, distance):
	baselink = "http://service.iris.edu/fdsnws/dataselect/1/query"
	timeshift = floor(distance/6) # Speed of seismic waves is between 2 and 6 km/s
	print(datetime.strftime((eventTime - relativedelta(seconds=timeshift)), isoDatetimeFormat))
	print(datetime.strftime((eventTime + relativedelta(seconds=300-timeshift)), isoDatetimeFormat))
	params = {
		"format":"sac.zip",
		"start":datetime.strftime((eventTime - relativedelta(seconds=timeshift)), isoDatetimeFormat),
		"end":datetime.strftime((eventTime + relativedelta(seconds=300-timeshift)), isoDatetimeFormat),
		"net":networkId,
		"sta":stationId
	}
	return requests.get(baselink, params)

def requestMultipleSacs(stations, event):
	requests = []
	for i in range(len(stations)):
		requests.append(requestSac(
			stations[i]["Network"],
			stations[i]["Station"],
			datetime.strptime(event['Time'], isoDatetimeFormat),
			distance(float(stations[i]['Longitude']), float(stations[i]['Latitude']), float(event['Longitude']), float(event['Latitude']))
		))
	return requests