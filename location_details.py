import requests
from requests.structures import CaseInsensitiveDict

API_KEY = "MY_API_KEY"


def get_location_details(location):
	INPUT = location
	url = f"https://api.geoapify.com/v1/geocode/search?text={INPUT}&apiKey={API_KEY}"

	headers = CaseInsensitiveDict()
	headers["Accept"] = "application/json"

	resp = requests.get(url, headers=headers)

	data_dict = resp.json()

	if "features" in data_dict and data_dict["features"]:
		result = data_dict["features"][0]
		latitude = result["properties"]["lat"]
		longitude = result["properties"]["lon"]
		adress = result["properties"]["formatted"]
		data = [adress, latitude, longitude]
		return data
	else:
		return None



