####################
# External modules
import obspy
import zipfile as zf
from datetime import datetime
from tabulate import tabulate
import os

####################
# Internal modules
# WAV export with amplifier
from sacToWav import sacToWav
# Sage API requests creators
from sage_requests import *
# geoCSV parser
from geocsv import geoCSVToDictArray

# Different datetime format used by the API
isoDatetimeFormat = '%Y-%m-%dT%H:%M:%SZ'
stationDatetimeFormat = '%Y-%m-%dT%H:%M:%S.%f'
fileDatetimeFormat = '%Y.%m.%d.%H.%M.%S'

####################
# Utility

# Save a string in a file
def saveFile(content, path):
	with open(path, "wb") as file:
	    file.write(content)

# Unzip only the first file in the zip
def unzip(path, destPath):
	with zf.ZipFile(path) as zip_ref:
		result = zip_ref.namelist()[0]
		zip_ref.extractall(destPath, members=[result])
	return result

# Print a dictionnary in a human-readable way
def printDict(lastEvents: [any]):
	print(tabulate(lastEvents, headers="keys", showindex="always"))

####################
# main
def main(howManyEvents = 5, howManyStations = 5):
	print("STARTING...")

	# Filename generators
	filename = lambda filebasename: filebasename + ".sac"
	zipname = lambda filebasename: filebasename + ".sac.zip"
	wavfilename = lambda filebasename: filebasename + ".wav"
	
	generatefilebasename = lambda s: f"{s['Network']}.{s['Station']}.{datetime.strftime(datetime.strptime(s['StartTime'], stationDatetimeFormat), fileDatetimeFormat)}"

	####################
	# Get last events
	print("GETTING LAST EVENTS")
	r = requestLastEvents(howManyEvents)
	if(r.status_code != 200):
		print("ERROR, LAST EVENTS REQUEST FAILED... STATUS :", r.status_code)
		exit()
	lastEvents = geoCSVToDictArray(r.content.decode("utf-8"))
	printDict(lastEvents)
	
	####################
	# Prompt for event selection
	eventSelected = int(input(f"Choose an event (between 0 and {howManyEvents-1}, -1 to quit) : "))
	while(eventSelected < -1 or eventSelected >= howManyEvents):
		eventSelected = int(input(f"Please select a valid event !\nChoose an event (between 0 and {howManyEvents-1}, -1 to quit) : "))
	if(eventSelected == -1):
		exit()

	####################
	# Request nearest stations
	eventTime = datetime.strptime(lastEvents[eventSelected]['Time'], isoDatetimeFormat)
	r = requestNearestStations(
		lastEvents[eventSelected]['Latitude'],
		lastEvents[eventSelected]['Longitude'],
		eventTime
	)
	stations = geoCSVToDictArray(r.content.decode("utf-8"))[:howManyStations]
	printDict(stations)

	####################
	# Request sac files for each station found
	print("GETTING SAC FILES")
	rs = requestMultipleSacs(stations, lastEvents[eventSelected])
	resultArray = []

	# Prompt for generation of wav files
	generateWav = input("GENERATE WAV FILES ? [y/n] ") == 'y'

	# Delete already existing sac files (as zip aren't deleted they can be manually unzipped if needed)
	for fileToDelete in os.listdir('sac'):
		os.remove(os.path.join('sac', fileToDelete))

	# Iterate through received zips
	triggerNothingToProcess = True
	for i in range(len(rs)):
		print(f"PROCESSING INDEX {i}")

		if(rs[i].status_code != 200):
			print("ERROR, SAC FILE REQUEST FAIL... STATUS :", rs[i].status_code)
			# Sometimes (often), stations are up, but 'Ressource not found'.
			if(rs[i].status_code == 204):
				print("IT SEEMS THAT THIS STATION WAS UP BUT NOTHING WAS RECORDED...")
			# If we can't process this station's result, some information is printed for debugging
			print(f"STATION WAS {stations[i]['Station']}, LOCATED AT LAT: {stations[i]['Latitude']}, LON: {stations[i]['Longitude']}")
			print(f"REQUEST: {rs[i].request.url}")
			print(f"RESULT: {rs[i].content}")
		else:
			triggerNothingToProcess = False
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

			# print(resultArray[-1][0].stats.sampling_rate)
	
	# All your results are in resultArray !
	return resultArray

if __name__ == "__main__":
	main(5,10)