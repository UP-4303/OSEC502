import requests
import obspy
import zipfile as zf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import os

from sacToWav import sacToWav

now = datetime.now()
isoDatetimeFormat = '%Y-%m-%dT%H:%M:%SZ'
stationDatetimeFormat = '%Y-%m-%dT%H:%M:%S.%f'
fileDatetimeFormat = '%Y.%m.%d.%H.%M.%S'

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

def saveFile(content, path):
	with open(path, "wb") as file:
	    file.write(content)

def unzip(path, destPath):
	with zf.ZipFile(path) as zip_ref:
		result = zip_ref.namelist()[0]
		zip_ref.extractall(destPath, members=[result])
	return result

def parseGeoCsvString(string: str):
	res = []
	lines = string.split("\n")

	for i in range(len(lines)):
		if(not lines[i].startswith('#')):
			res.append(lines[i].split('|'))
	return res[:-1]

def csvArrayToDictArray(csvArray):
	if(len(csvArray) <= 1):
		return []

	res = []
	headers = csvArray[0]
	csvArray = csvArray[1:]

	for i in range(len(csvArray)):
		res.append({})
		for j in range(len(headers)):
			res[i][headers[j]] = csvArray[i][j]
	return res

def geoCSVToDictArray(string: str):
	return csvArrayToDictArray(parseGeoCsvString(string))

def selectEventMenuCLI(lastEvents: [any]):
	print(tabulate(lastEvents, headers="keys", showindex="always"))

def main():
	print("STARTING...")

	filename = lambda filebasename: filebasename + ".sac"
	zipname = lambda filebasename: filebasename + ".sac.zip"
	wavfilename = lambda filebasename: filebasename + ".wav"
	
	generatefilebasename = lambda s: f"{s['Network']}.{s['Station']}.{datetime.strftime(datetime.strptime(s['StartTime'], stationDatetimeFormat), fileDatetimeFormat)}"

	howManyEvents = 5
	howManyStations = 2

	print("GETTING LAST EVENTS")
	r = requestLastEvents(howManyEvents)
	if(r.status_code != 200):
		print("ERROR, LAST EVENTS REQUEST FAILED... STATUS :", r.status_code)
		exit()
	lastEvents = geoCSVToDictArray(r.content.decode("utf-8"))
	selectEventMenuCLI(lastEvents)
	
	eventSelected = int(input(f"Choose an event (between 0 and {howManyEvents-1}, -1 to quit) : "))
	while(eventSelected < -1 and eventSelected >= howManyEvents):
		eventSelected = int(input(f"Please select a valid event !\nChoose an event (between 0 and {howManyEvents-1}, -1 to quit) : "))
	if(eventSelected == -1):
		exit()

	eventTime = datetime.strptime(lastEvents[eventSelected]['Time'], isoDatetimeFormat)
	
	generateWav = input("GENERATE WAV FILES ? [y/n] ") == 'y'

	r = requestNearestStations(
		lastEvents[eventSelected]['Latitude'],
		lastEvents[eventSelected]['Longitude'],
		eventTime
	)
	stations = geoCSVToDictArray(r.content.decode("utf-8"))[:howManyStations]

	selectEventMenuCLI(stations)

	print("GETTING SAC FILES")
	rs = requestMultipleSacs(stations, eventTime)
	resultArray = []

	for fileToDelete in os.listdir('sac'):
		os.remove(os.path.join('sac', fileToDelete))

	for i in range(len(rs)):
		print(f"PROCESSING INDEX {i}")

		if(rs[i].status_code != 200):
			print("ERROR, SAC FILE REQUEST FAIL... STATUS :", rs[i].status_code)
			if(rs[i].status_code == 204):
				print("IT SEEMS THAT THIS STATION WAS UP BUT NOTHING WAS RECORDED...")
			print(f"STATION WAS {stations[i]['Station']}, LOCATED AT LAT: {stations[i]['Latitude']}, LON: {stations[i]['Longitude']}")
			print(f"REQUEST: {rs[i].request.url}")
			print(f"RESULT: {rs[i].content}")
		else:
			print("SAVING ZIP FILE")
			filebasename = generatefilebasename(stations[i])
			
			saveFile(rs[i].content, "saczip/" + zipname(filebasename))

			print("UNZIPPING")
			tempFileName = unzip("saczip/" + zipname(filebasename), "sac")

			os.rename(os.path.join("sac", tempFileName), os.path.join("sac", filename(filebasename)))

			print("OPENING")
			resultArray.append(obspy.read("sac/" + filename(filebasename)))

			if (generateWav):
				print("GENERATING WAV FILE")
				sacToWav(resultArray[-1], 'wav/'+ wavfilename(filebasename))

if __name__ == "__main__":
	main()