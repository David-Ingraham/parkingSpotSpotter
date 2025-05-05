from get_nearby_cameras import find_nearby_cameras, haversine, get_geocode
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, send_file, make_response, Response
from fetch_image import fetch_and_save_image
import time
from io import BytesIO
import base64
from PIL import Image


app = Flask(__name__)

@app.post("/photo")
def photo():
    data = request.get_json()
    print(f'\nthis data was recived:\n{data}')
   # address = data.get("address", "")
    #print(f"\n\nReceived address: {address}")
    load_dotenv(dotenv_path='.env')
    google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
    camera_data_file = 'camera_id_lat_lng_wiped.json'

    user_lat = data['lat']
    user_lng = data['lng']

    #print(data['lat'])


    cameras = find_nearby_cameras(user_lat, user_lng, camera_data_file, google_maps_api_key)

    if not cameras:
        return f'sorry no cameras nearby'
    
    else:
        print(cameras)
    
    #print(f'nearby cameras:\n{cameras}')
    cam_id =  list(cameras.values())[0]["camera_id"] #just returning first id of neaby 
    #cameras. will change to pull all five out.
    #will loop over all 5 ids and call fetch_img on each. send each image out to cleint 
    print(f'\n\n\ncamera id is : {cam_id}')

    timestamp =int(time.time())


    cam_id_list = []
    for cam in cameras.keys():
        cam_id_list.append(cameras[cam]['camera_id'])

 
  

    

    img = fetch_and_save_image(camera_id=cam_id, timestamp=timestamp)


  

    buf = BytesIO()
    max_w = 640
    if img.width > max_w:                     # keep aspect ratio
        h = int(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)       # high‑quality resample :contentReference[oaicite:0]{index=0}

    img.save(buf, format="JPEG", quality=75, optimize=True)   # smaller file :contentReference[oaicite:1]{index=1}
    payload = buf.getvalue()

    return Response(payload,
                    mimetype="image/jpeg",
                    headers={"Content-Length": str(len(payload))})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
