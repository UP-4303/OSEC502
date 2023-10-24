import requests

def generateRequest():
    baselink = "http://service.iris.edu/fdsnws/dataselect/1/query"

if __name__ == "__main__":
    r = requests.get("http://service.iris.edu/fdsnws/dataselect/1/query?net=IU&sta=ANMO&loc=00&cha=BHZ&start=2010-02-27T06:30:00.000&end=2010-02-27T10:30:00.000")
    print(r.status_code)

    with open('test.mseed', 'wb') as file:
        file.write(r.content)