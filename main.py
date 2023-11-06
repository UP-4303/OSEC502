import requests
import obspy
import zipfile as zf
from sacToWav import sacToWav
from datetime import datetime

def requestLastEvents(howMany):
	now = datetime.now()

	baselink = "https://service.iris.edu/fdsnws/event/1/query"
	params = {
		"limit":str(howMany),
		"orderby":"time",
		"format":"geocsv",
		"start":str(now.replace(year=now.year-2).date()),
		"end":str(now.date())
	}
	return requests.get(baselink, params)

def requestSac():
	baselink = "http://service.iris.edu/fdsnws/dataselect/1/query"
	params = {
		"format":"sac.zip",
		"start":"2010-02-27T06:30:00.000",
		"end":"2010-02-27T10:30:00.000",
		"net":"IU",
		"sta":"ANMO",
		"loc":"00",
		"cha":"BHZ"
	}
	return requests.get(baselink, params)

def saveFile(content, path):
	with open(path, "wb") as file:
	    file.write(content)

def unzip(path, destPath):
	with zf.ZipFile(path) as zip_ref:
		zip_ref.extractall(destPath)

def parseGeoCsvString(string: str):
	res = []
	lines = string.split("\n")

	for i in range(len(lines)):
		res.append(lines[i].split('|'))
	return res[4:-1]

def main():
	print("STARTING...")
	filebasename = "IU.ANMO.00.BHZ.M.2010.058.063000"
	filename = filebasename + ".sac"
	zipname = filebasename + ".sac.zip"
	wavfilename = filebasename + ".wav"

	print("GETTING LAST EVENTS")
	r = requestLastEvents(5)
	if(r.status_code != 200):
		print("ERROR, REQUEST FAIL... STATUS :", r.status_code)
		exit
	print(parseGeoCsvString(r.content.decode("utf-8")))

	print("SENDING REQUEST")
	r = requestSac()
	if(r.status_code != 200):
		print("ERROR, REQUEST FAIL... STATUS :", r.status_code)
		exit

	print("SAVING ZIP FILE")
	saveFile(r.content, "saczip/"+zipname)

	print("UNZIPPING")
	unzip("saczip/"+zipname, "sac")

	print("OPENING")
	st = obspy.read("sac/"+filename)

	if(input("GENERATE WAV FILE ? [y/n]") == 'y'):
		print("GENERATING WAV FILE")
		sacToWav(st, 'wav/'+wavfilename)

	print("PLOTING")
	st.plot()

if __name__ == "__main__":
	r = requestLastEvents(5)
	print(r.status_code)
	print(parseGeoCsvString(r.content.decode("utf-8")))