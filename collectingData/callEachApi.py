from fetch_image import fetch_and_save_image, load_camera_data
import time
from sanitize_address import sanitize

from datetime import datetime, timezone

utc_now = datetime.now(timezone.utc)

camera_data = load_camera_data("camera_id_lat_lng_wiped.json")




for address, camera in camera_data.items():

    print(f'addres :{address}')

    print(f'camer :{camera}') 
    address = sanitize(address)

    fetch_and_save_image(camera,utc_now, address)




