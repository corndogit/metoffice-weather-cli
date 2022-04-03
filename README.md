# weather-cli
An open-source Python-based Met Office DataHub API grabber that returns 
weather data for a specified city.

## Usage
To use this program, you must have a Met Office Weather DataHub API key and
a geocode.xyz Auth token. These can be inserted into a .env file placed 
in the program directory as such:
```
# met office weather datahub
DATAHUB_API_KEY=xxxxxxxx
DATAHUB_SECRET=xxxxxxxx

#geocode.xyz
GEOCODE_AUTH=xxxxxxxx
```
Run `weather.py` in the console and type a city name when prompted. This will return the 
latitude and longitude coordinates of the city from the geocode.xyz API, which is then parsed into 
the GET url for the Met Office DataHub API . The data from this API is dumped into a .json file 
and contains a trove of daily weather information about the area.

## Example data

**geocode.xyz request as .JSON:**
![geocode.xyz JSON](https://corndog.s-ul.eu/l57ZgJ4i)

**Met Office Weather DataHub request as JSON:**
![met office datahub JSON](https://corndog.s-ul.eu/a4u1qsRi)

More data not included in this image.

##Todo

- Pick 'useful' information out of the Met Office data and present it in a 
human-readable format, starting with a simple .xls spreadsheet
- Add exception handling for API request timeouts, key errors (e.g. when geocoding
coordinates for a country) and invalid city names.
- Decode [Significant Weather Codes](https://www.metoffice.gov.uk/services/data/datapoint/code-definitions) into weather type (e.g. 7 = cloudy)

### Known Bugs

The program throws an exception for names of countries, so only city names 
can be input.
