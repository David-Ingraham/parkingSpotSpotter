import json
import requests
from PIL import Image
from io import BytesIO

def fetch_and_save_image(camera_id, time: int):
    api_url = f'https://webcams.nyctmc.org/api/cameras/{camera_id}/image?t={time}'

    response = requests.get(api_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save('traffic_camera_image.png')
        print("Image saved as traffic_camera_image.png")
    else:
        print(f"Error: Could not fetch image. Status Code: {response.status_code}")

def main():
    try:
        with open('camera_data.json', 'r') as f:
            camera_data = json.load(f)
    except FileNotFoundError:
        print("Error: camera_data.json file not found. Please run the scraping script first.")
        return

    address = input("Enter an address in NYC (e.g., '1 Ave @ 110 St'): ")

    camera_id = camera_data.get(address)
    time = 0
    if camera_id:
        fetch_and_save_image(camera_id, time)
    else:
        print(f"No camera found for the address: {address}")

if __name__ == "__main__":
    main()
