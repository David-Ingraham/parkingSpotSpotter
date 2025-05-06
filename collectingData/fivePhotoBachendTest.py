from get_nearby_cameras import find_nearby_cameras, haversine, get_geocode
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, send_file, make_response, Response
from flask_cors import CORS
from fetch_image import fetch_and_save_image
import time
from io import BytesIO
import base64
from PIL import Image



app = Flask(__name__)

CORS(app)


@app.post("/photo")
def photo():
    data = request.get_json()
    user_lat, user_lng = data["lat"], data["lng"]

    cameras = find_nearby_cameras(user_lat, user_lng,
                                  "camera_id_lat_lng_wiped.json",
                                  os.getenv("GOOGLEMAPSAPI"))
    
    print(cameras)
    if not cameras:
        return jsonify(error="no cameras nearby"), 404

    imgs   = []
    stamp  = int(time.time())

    for addr, info in list(cameras.items())[:5]:          # first 5 only
        img = fetch_and_save_image(info["camera_id"], stamp)

        if img.width > 640:                               # keep aspect
            h = img.height * 640 // img.width
            img = img.resize((640, h), Image.LANCZOS)

        buf = BytesIO()
        img.save(buf, format="JPEG", quality=75, optimize=True)
        imgs.append({
            "address": addr,
            "photo": base64.b64encode(buf.getvalue()).decode()
        })

    print(jsonify(images=imgs))

    return jsonify(images=imgs)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)