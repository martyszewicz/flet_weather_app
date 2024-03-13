import datetime as dt
import pytz
import requests


class Weaher_details():
	def __init__(self, localisation):
		self.apikey = "9LXoLlnUWGWlYXGKfC2mZgdYnCZjDY76"
		self.localisation = [localisation[1], localisation[2]]
		self.url = "https://api.tomorrow.io/v4/timelines"
		self.units = "metric"
		self.timezone = "US/Eastern"
		self.now = dt.datetime.now(pytz.UTC)
		self.fields = [
			"temperature",
			"cloudCover",
			"temperatureApparent",
			"humidity",
			"windSpeed",
			"rainIntensity",
			"freezingRainIntensity",
			"snowIntensity",
		]

	def current_weather(self):
		timesteps = ["1h"]
		startTime = (self.now).isoformat()
		endTime = (self.now + dt.timedelta(hours=24)).isoformat()
		body = {"location": self.localisation, "fields": self.fields, "units": self.units, "timesteps": timesteps,
				"startTime": startTime,
				"endTime": endTime, "timezone": self.timezone}
		try:
			response = requests.post(f'{self.url}?apikey={self.apikey}', json=body)
			data = response.json()
			return data
		except Exception as e:
			print("An error occurred:", e)

	def daily_weather(self):
		self.params = self.fields + ["sunriseTime", "sunsetTime"]
		timesteps = ["1d"]
		startTime = (self.now).isoformat()
		endTime = (self.now + dt.timedelta(days=5)).isoformat()
		body = {"location": self.localisation, "fields": self.params, "units": self.units, "timesteps": timesteps,
				"startTime": startTime,
				"endTime": endTime, "timezone": self.timezone}
		try:
			response = requests.post(f'{self.url}?apikey={self.apikey}', json=body)
			data = response.json()
			return data
		except Exception as e:
			print("An error occurred:", e)