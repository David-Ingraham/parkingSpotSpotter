import json
import requests
from dotenv import load_dotenv
import os

def get_geocode(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    results = response.json()
    print(f"API Response for {address}: {results}")  # Debug: Print the entire API response
    if results.get('results'):
        address_components = results['results'][0].get('address_components')
        geometry = results['results'][0].get('geometry', {}).get('location', {})
        lat = geometry.get('lat')
        lng = geometry.get('lng')
        zip_code = None
        for component in address_components:
            if 'postal_code' in component.get('types'):
                zip_code = component.get('long_name')
        return zip_code, lat, lng
    return None, None, None

def update_addresses(input_file, output_file, api_key):
    try:
        with open(input_file, 'r') as f:
            addresses = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON input: {e}")
        return

    updated_addresses = {}
    for key, value in addresses.items():
        full_address = f"{key}, New York, NY"
        print(f"Processing: {full_address}")
        zip_code, lat, lng = get_geocode(full_address, api_key)
        if zip_code and lat and lng:
            updated_key = f"{full_address} {zip_code}"
            print(f"Updated Address: {updated_key}")
            updated_addresses[updated_key] = {
                "camera_id": value,
                "latitude": lat,
                "longitude": lng
            }
        else:
            updated_addresses[full_address] = {
                "camera_id": value,
                "latitude": None,
                "longitude": None
            }

    try:
        with open(output_file, 'w') as f:
            json.dump(updated_addresses, f, indent=4)
    except Exception as e:
        print(f"Failed to write JSON output: {e}")

# Usage
load_dotenv(dotenv_path='../.env')

input_file = 'camera_loc_test.json'
output_file = 'output_addresses.json'
google_maps_api_key = os.getenv('GOOGLEMAPSAPI')

if google_maps_api_key:
    try:
        update_addresses(input_file, output_file, google_maps_api_key)
    except Exception as e:
        print(f"Update address function did not run: {e}")
else:
    print("Google Maps API key not found in environment variables.")
