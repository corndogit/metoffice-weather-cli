import os
from dotenv import load_dotenv   # fetch API_KEY and SECRET from .env
import http.client
from sys import argv   # for testing purposes only

script, latitude, longitude = argv   # todo find geolocation/geocoding api to fetch lat/long from 

load_dotenv()

conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

headers = {
    'X-IBM-Client-Id': os.getenv('API_KEY'),
    'X-IBM-Client-Secret': os.getenv('SECRET'),
    'accept': "application/json"
    }


conn.request("GET", f"/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=true&latitude={latitude}&longitude={longitude}", headers=headers)

res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8"))

dump = open('dump.json', 'wb')
dump.write(data)
print("Data written to dump.json")
dump.close()