import os
from dotenv import load_dotenv, find_dotenv  # fetch API_KEYs and SECRET from .env
import http.client
import urllib.parse
import json
from weathercodes import decode_weather_type, decode_uv_index

load_dotenv(find_dotenv())


def get_geolocation(location):
    # connect to geocoding API
    connection = http.client.HTTPSConnection("geocode.xyz")
    params = urllib.parse.urlencode({
        'auth': os.getenv('GEOCODE_AUTH'),
        'locate': location,
        'json': 1
    })

    connection.request("GET", "/?{}".format(params))

    geocode_res = connection.getresponse()
    geocode_json = json.loads(geocode_res.read())  # reads JSON file from response

    if 'error' in geocode_json:
        raise KeyError("API error - your request produced no suggestions.")
    return geocode_json


def get_weather_info(geocode_dict):
    params = (
        geocode_dict['standard']['city'],
        geocode_dict['standard']['countryname'],
        geocode_dict['latt'],
        geocode_dict['longt']
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
        'latitude': params[2],
        'longitude': params[3]
    })

    datahub_conn.request('GET',
                         '/metoffice/production/v0/forecasts/point/daily?{}'.format(datahub_params),
                         headers=datahub_headers
                         )

    datahub_res = datahub_conn.getresponse()
    datahub_json = json.loads(datahub_res.read())

    time_series = datahub_json['features'][0]['properties']['timeSeries'][1]

    weather_data = {
        "City": params[0],
        "Country": params[1],
        "TimeOfModel": time_series['time'],
        "WeatherType": decode_weather_type(time_series['daySignificantWeatherCode']),
        "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
        "MinTemperature": time_series['dayLowerBoundMaxTemp'],
        "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'],  # %
        "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
        "MaxUvIndex": time_series['maxUvIndex']
    }
    return weather_data


def print_results(data):
    # todo: control which options are printed as determined by args
    print(f"Weather for {data['City']}, {data['Country']}")
    print(f"Weather: {data['WeatherType']}")
    print(f"Max temp: {round(data['MaxTemperature'])} degrees Celsius")
    print(f"Min temp: {round(data['MinTemperature'])} degrees Celsius")
    print(f"Chance of precipitation: {data['ChanceOfPrecipitation']}%")
    print(f"Wind speed: {round(float(data['WindSpeed'] / 0.44704), 1)} mph")
    print(f"Peak UV Index: {data['MaxUvIndex']} ({decode_uv_index(data['MaxUvIndex'])})")


if __name__ == '__main__':
    print("Please enter desired city:")
    stdin = input("> ")
    result = get_weather_info(get_geolocation(stdin))
    print_results(result)
