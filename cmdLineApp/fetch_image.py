import json
import requests
from PIL import Image
from io import BytesIO
import time

def fetch_and_save_image(camera_id, timestamp):
    api_url = f'https://webcams.nyctmc.org/api/cameras/{camera_id}/image?t={timestamp}'

    response = requests.get(api_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(f'traffic_camera_image_{camera_id}_{timestamp}.png')
        print(f"Image saved as traffic_camera_image_{camera_id}_{timestamp}.png")
    else:
        print(f"Error: Could not fetch image. Status Code: {response.status_code}")

def main():
    try:
        with open('camera_addresses_to_id.json', 'r') as f:
            camera_data = json.load(f)
    except FileNotFoundError:
        print("Error: camera_addresses_to_id.json file not found. Please run the scraping script first.")
        return
    except json.JSONDecodeError:
        print("Error: JSON file is malformed.")
        return

    address = input("Enter an address in NYC (e.g., '1 Ave @ 110 St'): ")

    camera_id = camera_data.get(address)
    if camera_id:
        timestamp = int(time.time() * 1000)
        fetch_and_save_image(camera_id, timestamp)
    else:
        print(f"No camera found for the address: {address}")

if __name__ == "__main__":
    main()
