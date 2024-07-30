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
        img.save(f'traffic_camera_images/traffic_camera_image_{camera_id}_{timestamp}.png')
        print(f"Image saved as traffic_camera_image_{camera_id}_{timestamp}.png")
    else:
        print(f"Error: Could not fetch image. Status Code: {response.status_code}")

def load_camera_data():
    try:
        with open('camera_addresses_to_id.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: camera_addresses_to_id.json file not found. Please run the scraping script first.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON file is malformed.")
        return None

