import json
import requests
from PIL import Image
from io import BytesIO
import time
from sanitize_address import sanitize

def fetch_and_save_image(camera_id, timestamp):

    try:
        api_url = f'https://webcams.nyctmc.org/api/cameras/{camera_id}/image?t={timestamp}'

        response = requests.get(api_url)
        #rint(address)
        numErrs = 0
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            #imgFilePath = f'traffic_camera_images/{(camera_id)}.png'
            #img.save(imgFilePath)
            #print(f"Image saved as {imgFilePath}")
        else:
            print(f"Error: Could not fetch image. Status Code: {response.status_code}")
            numErrs +=1

       

    except:
        print("one got messed up by we are intrepid")

    return img

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



def main():
    id = "23994d9e-7e59-4808-8d47-405f779d19cf"
    timestamp =int(time.time())


    fetch_and_save_image(id, timestamp)



if __name__ == "__main__":
    main()