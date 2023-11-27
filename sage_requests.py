from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

now = datetime.now()

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

def requestSac(networkId, stationId, eventTime):
	baselink = "http://service.iris.edu/fdsnws/dataselect/1/query"
	params = {
		"format":"sac.zip",
		"start":str((eventTime - relativedelta(minute=5)).date()),
		"end":str((eventTime + relativedelta(minute=5)).date()),
		"net":networkId,
		"sta":stationId
	}
	return requests.get(baselink, params)

def requestMultipleSacs(stations, eventTime):
	requests = []
	for i in range(len(stations)):
		requests.append(requestSac(stations[i]["Network"], stations[i]["Station"], eventTime))
	return requests