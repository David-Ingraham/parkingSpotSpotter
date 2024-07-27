import json
from geopy.distance import geodesic
from opencage.geocoder import OpenCageGeocode

# Replace 'YOUR_API_KEY' with your actual OpenCage API key
OPENCAGE_API_KEY = 'YOUR_API_KEY'

def geocode_address(address):
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    result = geocoder.geocode(address)
    if result:
        return (result[0]['geometry']['lat'], result[0]['geometry']['lng'])
    else:
        raise ValueError(f"Address '{address}' not found.")

def get_addresses_within_radius(json_file_path, user_address, radius_miles=1):
    # Get user coordinates
    user_lat, user_lon = geocode_address(user_address)

    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    addresses_within_radius = []

    for item in data:
        address = item.get('address')
        if address:
            try:
                lat, lon = geocode_address(address)
                item['latitude'] = lat
                item['longitude'] = lon
            except ValueError as e:
                print(f"Could not geocode address: {address}. Error: {e}")
                continue
            
            # Calculate distance
            distance = geodesic((user_lat, user_lon), (lat, lon)).miles
            if distance <= radius_miles:
                addresses_within_radius.append(address)
    
    return addresses_within_radius

if __name__ == "__main__":
    # Example JSON file path
    json_file_path = 'addresses.json'
    
    # User input for address
    user_address = input("Enter your address: ")

    try:
        # Get addresses within the radius
        result = get_addresses_within_radius(json_file_path, user_address)
        
        if result:
            print("Addresses within 1 mile radius:")
            for address in result:
                print(address)
        else:
            print("No addresses found within 1 mile radius.")
    except ValueError as e:
        print(e)
