import os
from dotenv import load_dotenv  # fetch API_KEYs and SECRET from .env
import http.client
import urllib.parse
import json
from doc.weathercodes import weathercodes, decode_uv_index

load_dotenv()
print("Please enter desired city:")
while True:
    location = input("> ")

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

    if 'error' in geocode_json:
        print("API error - your request produced no suggestions.")
    else:
        break

geocode_values = (
    geocode_json['standard']['city'],
    geocode_json['standard']['countryname'],
    geocode_json['latt'],
    geocode_json['longt']
)


# connect to Weather DataHub
datahub_conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

datahub_headers = {
    'X-IBM-Client-Id': os.getenv('DATAHUB_API_KEY'),
    'X-IBM-Client-Secret': os.getenv('DATAHUB_SECRET'),
    'accept': "application/json"
}

datahub_params = urllib.parse.urlencode({
    'excludeParameterMetadata': 'true',
    'includeLocationName': 'true',
    'latitude': geocode_values[-2],
    'longitude': geocode_values[-1]
})

datahub_conn.request('GET',
                     '/metoffice/production/v0/forecasts/point/daily?{}'.format(datahub_params),
                     headers=datahub_headers
                     )

datahub_res = datahub_conn.getresponse()
datahub_json = json.loads(datahub_res.read())

time_series = datahub_json['features'][0]['properties']['timeSeries'][1]

weather_data = {
    "TimeOfModel": time_series['time'],
    "SignificantWeatherCode": time_series['daySignificantWeatherCode'],
    "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
    "MinTemperature": time_series['dayLowerBoundMaxTemp'],
    "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'],  # %
    "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
    "MaxUvIndex": time_series['maxUvIndex']
}
print(f"""
Weather for {geocode_values[0]}, {geocode_values[1]}:
Weather: {weathercodes[str(weather_data['SignificantWeatherCode'])]}
Max temp: {round(weather_data['MaxTemperature'])} degrees Celsius
Min temp: {round(weather_data['MinTemperature'])} degrees Celsius
Chance of precipitation: {weather_data['ChanceOfPrecipitation']}%
Wind speed: {round(float(weather_data['WindSpeed'] / 0.44704), 1)} mph
Peak UV Index: {weather_data['MaxUvIndex']} ({decode_uv_index(weather_data['MaxUvIndex'])})
""")
