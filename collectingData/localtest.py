from get_nearby_cameras import find_nearby_cameras, haversine, get_geocode
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.post("/photo")
def photo():
    data = request.get_json()
    address = data.get("address", "")
    print(f"Received address: {address}")
    load_dotenv(dotenv_path='.env')
    google_maps_api_key = os.getenv('GOOGLEMAPSAPI')
    camera_data_file = 'camera_id_lat_lng_wiped.json'

    cameras = find_nearby_cameras(address, camera_data_file, google_maps_api_key)
    print(cameras)
    return jsonify({
        "status": "ok",
        "message": f"{len(cameras)} cameras found",
        "cameras": cameras
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
