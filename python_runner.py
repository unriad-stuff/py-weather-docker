from datetime import datetime
from threading import Timer
from pymongo import MongoClient
import urllib.request as request
import json
from datetime import datetime as dt
import configparser

x=datetime.today()
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

onfig = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['KEY']
url = config['API']['URL']
MONGO_URL = config['DATABASE']['URL']


def update_database(forecast_collection, forecast):
	fore_date = dt.fromtimestamp(forecast['time'])
	today_date = dt.now()
	forecasted_day = fore_date.strftime("%Y-%m-%d")

	days_before = '{} day'.format((fore_date - today_date).days)

	location = forecast_collection.find_one({'lat':forecast['location']['lat'], 'lon':forecast['location']['lon']})
	if location is None:
		location  = {'lat':forecast['location']['lat'], 'lon':forecast['location']['lon'], 'forecasts': {}}
	if forecasted_day not in location['forecasts'].keys():
		location['forecasts'][forecasted_day] = {}
	# check to prevent duplicates
	if days_before not in location['forecasts'][forecasted_day].keys():
		location['forecasts'][forecasted_day][days_before] = forecast
		forecast_collection.save(location)


def get_forecast(lon, lat):
	location_url = url.format(lon,lat)
	print(location_url)
	src = request.urlopen(location_url).read()
	weather = json.loads(src)
	forecast = weather['daily']['data']

	return forecast

def get_points():
	points = []
	with open('points.csv', 'r') as file:
		lines = file.read().split('\n')
		for row in lines:
			points.append(row.split(','))
	return points

def __main__():

	client = MongoClient(MONGO_URL)
	weather_db = client.weather
	forecast_collection = weather_db.forecasts

	for p in get_points()[:3]:
		dailies = get_forecast(*p)
		for forecast in dailies:
				forecast['location'] = {'lon':p[0], 'lat':p[1]}
				update_database(forecast_collection, forecast)


if __name__ == '__main__':
	__main__()


t = Timer(secs, __main__)
t.start()
