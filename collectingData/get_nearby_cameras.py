import json
import requests
from dotenv import load_dotenv
import os
from math import radians, cos, sin, asin, sqrt
from haversine import haversine




def get_geocode(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
            "components": "country:US|administrative_area:NY|locality:New York",
            "bounds": "40.477399,-74.259090|40.917577,-73.700272",
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

def find_nearby_cameras(user_lat, user_lng, camera_data_file, api_key, radius=2):
    
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
    user_lat_lngt = (user_lat, user_lng)

    print(user_lat_lngt)
   #print(camera_data[user_address])
    
    for address, details in camera_data.items():
        camera_lat = details.get('latitude')
        camera_lng = details.get('longitude')
        camera_lat_lng = (camera_lat, camera_lng)
        if camera_lat is not None and camera_lng is not None:
            distance = haversine(user_lat_lngt,camera_lat_lng)
           #print(f'addy: {address}   lat : {camera_lat}    long : {camera_lng}   distance : {distance} ')
            if distance <= radius:
                nearby_cameras[address] = details

    return nearby_cameras

# Usage
load_dotenv(dotenv_path='.env')
google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
camera_data_file = 'camera_id_lat_lng_wiped.json'
addy =   "park ave 86 st"
addy2 = "10_Ave_42_St"

#data = get_geocode("11_Ave_42_St", google_maps_api_key)#
#ata = find_nearby_cameras(addy, 'camera_id_lat_lng_wiped.json', google_maps_api_key)

#ata2= find_nearby_cameras(addy2,'camera_id_lat_lng_wiped.json', google_maps_api_key)
#rint(f' \n Dictionary of closests cams: {data} \n')


   #print(find_nearby_cameras(addy, camera_data_file, google_maps_api_key))

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


