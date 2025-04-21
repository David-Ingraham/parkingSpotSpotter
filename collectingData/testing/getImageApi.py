import requests
from PIL import Image
from io import BytesIO

# Example API endpoint URL (replace with the actual URL you found)
api_url = 'https://webcams.nyctmc.org/api/cameras/38c07664-0329-471e-997f-6a9015a5bcef/image?t=1721924729330'

# Fetch the image from the API
response = requests.get(api_url)
if response.status_code == 200:
    # Load the image into PIL
    img = Image.open(BytesIO(response.content))

    # Save the image
    img.save('traffic_camera_image.png')
    print("Image saved as traffic_camera_image.png")
else:
    print(f"Error: Could not fetch image. Status Code: {response.status_code}")
