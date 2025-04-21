import json
import requests
from PIL import Image
from io import BytesIO
import time
from sanitize_address import sanitize

def fetch_and_save_image(camera_id, timestamp, address):

    try:
        api_url = f'https://webcams.nyctmc.org/api/cameras/{camera_id}/image?t={timestamp}'

        response = requests.get(api_url)
        print(address)
        numErrs = 0
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            imgFilePath = f'traffic_camera_images/{(address)}.png'
            img.save(imgFilePath)
            print(f"Image saved as {imgFilePath}")
        else:
            print(f"Error: Could not fetch image. Status Code: {response.status_code}")
            numErrs +=1

        print(numErrs)

    except:
        print("one got messed up by we are intrepid")

def load_camera_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: camera_addresses_to_id.json file not found. Please run the scraping script first.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON file is malformed.")
        return None

