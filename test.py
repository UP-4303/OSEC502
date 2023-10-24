import requests
import obspy
import zipfile as zf
from os import listdir

def sendRequest():
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

if __name__ == "__main__":
    filebasename = "IU.ANMO.00.BHZ.M.2010.058.063000"
    filename = filebasename + ".SAC"
    zipname = filebasename + '.sac.zip'

    r = sendRequest()
    print(r.status_code)

    with open(zipname, 'wb') as file:
        file.write(r.content)

    with zf.ZipFile(zipname, 'r') as zip_ref:
        zip_ref.extractall('test')

    st = obspy.read("test\\"+ listdir("test")[0])
    st.plot()