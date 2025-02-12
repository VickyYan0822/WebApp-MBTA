from config import MAPBOX_TOKEN, MBTA_API_KEY
import json
import pprint
import urllib.request

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """

    query = "Babson College"
    query = query.replace(
        " ", "%20"
    )  # In URL encoding, spaces are typically replaced with "%20"
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"
    print(url)  # Try this URL in your browser first

    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode("utf-8")
        response_data = json.loads(response_text)
        # pprint.pprint(response_data)
    return response_data


def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    query = place_name.replace(
        " ", "%20"
    )  # In URL encoding, spaces are typically replaced with "%20"
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode("utf-8")
        response_data = json.loads(response_text)
        # pprint.pprint(response_data)
        longtitude = response_data["features"][0]["center"][0]
        latitude = response_data["features"][0]["center"][1]
    return latitude, longtitude


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    # print(url)
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode("utf-8")
        response_data = json.loads(response_text)
        # pprint.pprint(response_data)
    station_name =  response_data["data"][0]["attributes"]["name"]
    wheelchair_accessible =  response_data["data"][0]["attributes"]["wheelchair_boarding"]
    return station_name, wheelchair_accessible


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longitude = get_lat_long(place_name)
    # print(latitude, longitude)
    url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    # print(url)
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode("utf-8")
        response_data = json.loads(response_text)
        # pprint.pprint(response_data)
    nearest_stop = response_data["data"][0]["attributes"]["name"]
    wheelchair_accessible = response_data["data"][0]["attributes"]["wheelchair_boarding"]
    return nearest_stop, wheelchair_accessible


def main():
    """
    You should test all the above functions here
    """
    response_data = get_json(MAPBOX_BASE_URL)
    print(response_data["features"][0]["properties"]["address"])
    print(get_lat_long("Babson College"))
    print(get_nearest_station(42.2809, -71.2376))
    print(find_stop_near("Koko FitClub of Needham"))


if __name__ == "__main__":
    main()
