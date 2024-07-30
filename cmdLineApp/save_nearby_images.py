import json
import requests
from dotenv import load_dotenv
import os
import time
from PIL import Image
from io import BytesIO
from math import radians, cos, sin, asin, sqrt

# Import functions from the existing scripts
from get_nearby_cameras import haversine, get_geocode, find_nearby_cameras
from fetch_image import fetch_and_save_image, load_camera_data

def main():
    # Load environment variables
    load_dotenv(dotenv_path='.env')
    google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
    
    if not google_maps_api_key:
        print("Google Maps API key not found in environment variables.")
        return

    # Get user input
    user_address = input("Enter the address: ")
    radius = float(input("Enter the radius in miles (default is 0.5 miles): ") or 0.5)

    # Load camera data
    camera_data_file = 'camera_id_lat_lng.json'
    try:
        with open(camera_data_file, 'r') as f:
            camera_data = json.load(f)
    except Exception as e:
        print(f"Failed to load camera data JSON: {e}")
        return

    # Find nearby cameras
    nearby_cameras = find_nearby_cameras(user_address, camera_data_file, google_maps_api_key, radius)
    
    if not nearby_cameras:
        print("No cameras found within the specified radius.")
        return

    # Fetch and save images
    timestamp = int(time.time())
    for address, details in nearby_cameras.items():
        camera_id = details['camera_id']
        fetch_and_save_image(camera_id, timestamp)

if __name__ == "__main__":
    main()
