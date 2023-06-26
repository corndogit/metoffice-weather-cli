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

### geocode.xyz request as .JSON:

![geocode.xyz JSON](https://corndog.s-ul.eu/l57ZgJ4i)

### Met Office Weather DataHub request as JSON:

![met office datahub JSON](https://corndog.s-ul.eu/a4u1qsRi)

More data not included in this image (file is 300+ lines long).

### Running the program

![runtime](https://corndog.s-ul.eu/QKSLqybH.gif)

## Todo

- Pick all 'useful' information out of the Met Office data - some is currently omitted
- Allow program to be run using argument parsing - let the user provide a city name or latitude/longitude co-ords themselves

