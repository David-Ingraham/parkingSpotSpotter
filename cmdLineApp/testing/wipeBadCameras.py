import json
import os

# Set your paths
json_path = '../data_cleaning/cleaned_json.json'
out_path ="../camera_id_lat_lng_wiped_test.json"
directory_with_files = '../traffic_camera_images'

# Load the JSON
with open(json_path, 'r') as f:
    data = json.load(f)

# Get the set of file names in the directory
existing_files = list(os.listdir(directory_with_files))

for i in range(len(existing_files)):
    existing_files[i] = existing_files[i].split(".")[0]
#print(existing_files)

# Filter the JSON data
filtered_dict = {k: data[k] for k in existing_files if k in data}

print(filtered_dict)

missing_cameras = [name for name in existing_files if name not in data]

for cam in missing_cameras:
    print(cam)



# (Optional) Overwrite the JSON file with filtered data
#ith open(out_path, "w") as f:
 #  json.dump(filtered_dict, f, indent=4)

print(f"Filtered JSON saved. \nOriginal count: {len(data)}\nAfter filter: {len(filtered_dict)}\n Num of good cameras: {len(existing_files)}")
