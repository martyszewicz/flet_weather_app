import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import pdb


class Weaher_details():
	def __init__(self, localisation):
		self.localisation = localisation
		self.url = "https://api.open-meteo.com/v1/forecast"
		self.cache_session = requests_cache.CachedSession('.cache', expire_after=10000)
		self.retry_session = retry(self.cache_session, retries=5, backoff_factor=2)
		self.openmeteo = openmeteo_requests.Client(session=self.retry_session)

	def current_weather(self):
		print("start current")
		self.params = {
			"latitude": self.localisation[1],
			"longitude": self.localisation[2],
			"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation",
						"rain", "showers", "snowfall", "cloud_cover", "wind_speed_10m"],
			"forecast_days": 1
		}
		print(type(self.params["latitude"]))
		try:
			print(f"{self.localisation[1], self.localisation[2]}")
			responses = self.openmeteo.weather_api(self.url, params=self.params)
			print(responses, "responses")
			response = responses[0]
			print(response, "response")
			current = response.Current()
			print(current, "current")
			current_temperature_2m = current.Variables(0).Value()
			current_relative_humidity_2m = current.Variables(1).Value()
			current_apparent_temperature = current.Variables(2).Value()
			current_is_day = current.Variables(3).Value()
			current_precipitation = current.Variables(4).Value()
			current_rain = current.Variables(5).Value()
			current_showers = current.Variables(6).Value()
			current_snowfall = current.Variables(7).Value()
			current_cloud_cover = current.Variables(8).Value()
			current_wind_speed_10m = current.Variables(9).Value()
			current_weather_details = [current.Time(), current_temperature_2m, current_relative_humidity_2m,
									   current_apparent_temperature, current_is_day, current_precipitation,
									   current_rain, current_showers, current_snowfall, current_cloud_cover,
									   current_wind_speed_10m]
			print(current_weather_details)
		except Exception as e:
			print("An error occurred:", e)





	def daily_weather(self):
		responses = self.openmeteo.weather_api(self.url, params=self.params)

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation {response.Elevation()} m asl")
		print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
		print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

		# Process daily data. The order of variables needs to be the same as requested.
		daily = response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

		daily_data = {"date": pd.date_range(
			start=pd.to_datetime(daily.Time(), unit="s", utc=True),
			end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
			freq=pd.Timedelta(seconds=daily.Interval()),
			inclusive="left"
		)}
		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["temperature_2m_min"] = daily_temperature_2m_min

		daily_dataframe = pd.DataFrame(data=daily_data)
		print(daily_dataframe)


def daily_weather(location):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 52.2298,
		"longitude": 21.0118,
		"daily": ["temperature_2m_max", "temperature_2m_min"]
	}
