from get_nearby_cameras import find_nearby_cameras, haversine, get_geocode
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, send_file, make_response
from fetch_image import fetch_and_save_image
import time
from io import BytesIO



app = Flask(__name__)

@app.post("/photo")
def photo():
    data = request.get_json()
    address = data.get("address", "")
    print(f"\n\nReceived address: {address}")
    load_dotenv(dotenv_path='.env')
    google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
    camera_data_file = 'camera_id_lat_lng_wiped.json'

    cameras = find_nearby_cameras(address, camera_data_file, google_maps_api_key)
    print(cameras)
    cam_id =  list(cameras.values())[0]["camera_id"] #just returning first id of neaby 
    #cameras. will change to pull all five out.
    #will loop over all 5 ids and call fetch_img on each. send each image out to cleint 
    print(f'\n\n\ncamera id is : {cam_id}')

    timestamp =int(time.time())
   
 

    img = fetch_and_save_image(camera_id=cam_id, timestamp=timestamp, address=address)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = make_response(send_file(buf, mimetype='image/png'))
    #esponse.headers["Content-Encoding"] = "identity"  # prevent compression
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
