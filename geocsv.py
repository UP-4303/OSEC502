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