import os
from dotenv import load_dotenv   # fetch API_KEYs and SECRET from .env
import http.client
import urllib.parse
import json


load_dotenv()

location = input("Please enter desired location:\t")

# connect to geocoding API
geocode_conn = http.client.HTTPSConnection("geocode.xyz")
geocode_params = urllib.parse.urlencode({
    'auth': os.getenv('GEOCODE_AUTH'),
    'locate': location,
    'json': 1
})

geocode_conn.request("GET", "/?{}".format(geocode_params))

geocode_res = geocode_conn.getresponse()
geocode_json = json.loads(geocode_res.read())  # reads JSON file from response

geocode_values = (
    geocode_json['standard']['city'],
    geocode_json['standard']['countryname'],
    geocode_json['latt'],
    geocode_json['longt']
)
print(geocode_values)

# connect to Weather DataHub
datahub_conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

headers = {
    'X-IBM-Client-Id': os.getenv('DATAHUB_API_KEY'),
    'X-IBM-Client-Secret': os.getenv('DATAHUB_SECRET'),
    'accept': "application/json"
    }


datahub_conn.request("GET", f"/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=true&latitude={geocode_values[2]}&longitude={geocode_values[3]}", headers=headers)

datahub_res = datahub_conn.getresponse()
datahub_json = datahub_res.read()


# data dump
with open('dump.json', 'wb') as datahub_dump:
    datahub_dump.write(datahub_json)
    print("Data written to dump.json")
    datahub_dump.close()
