import json
import requests
from dotenv import load_dotenv
import os
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in miles between two points 
    on the Earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956  # Radius of Earth in miles. Use 6371 for kilometers
    return c * r

def get_geocode(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        results = response.json()

        if results.get("status") != "OK":
            print(f"Geocode error: {results.get('status')} - {results.get('error_message')}")
            return None, None

        location = results["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]

    except Exception as e:
        print(f"Request failed: {e}")
        return None, None

def find_nearby_cameras(user_address, camera_data_file, api_key, radius=0.5):
    user_lat, user_lng = get_geocode(user_address, api_key)
    if user_lat is None or user_lng is None:
        print("Failed to get the geocode for the user address.")
        return

    try:
        with open(camera_data_file, 'r') as f:
            camera_data = json.load(f)
    except Exception as e:
        print(f"Failed to load camera data JSON: {e}")
        return

    nearby_cameras = {}
    for address, details in camera_data.items():
        camera_lat = details.get('latitude')
        camera_lng = details.get('longitude')
        if camera_lat is not None and camera_lng is not None:
            distance = haversine(user_lat, user_lng, camera_lat, camera_lng)
            if distance <= radius:
                nearby_cameras[address] = details

    return nearby_cameras

# Usage
load_dotenv(dotenv_path='.env')
google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
camera_data_file = 'camera_id_lat_lng_wiped.json'

#data = get_geocode("11_Ave_42_St", google_maps_api_key)

#print(data)

""" 
if google_maps_api_key:
    user_address = input("Enter the address: ")
    radius = float(input("Enter the radius in miles (default is 0.5 miles): ") or 0.5)
    nearby_cameras = find_nearby_cameras(user_address, camera_data_file, google_maps_api_key, radius)
    if nearby_cameras:
        print("Nearby Cameras:")
        print(json.dumps(nearby_cameras, indent=4))
    else:
        print("No cameras found within the specified radius.")
else:
    print("Google Maps API key not found in environment variables.")
"""


