import json
import os

# Set your paths
json_path = 'camera_id_lat_lng_TEST.json'        
directory_with_files = '../traffic_camera_images'

# Load the JSON
with open(json_path, 'r') as f:
    data = json.load(f)

# Get the set of file names in the directory
existing_files = set(os.listdir(directory_with_files))

for i in range(len(existing_files)):
    existing_files[i] = existing_files[i].split(".")[0]
#print(existing_files)

# Filter the JSON data
filtered_dict = {k: data[k] for k in existing_files if k in data}

print(filtered_dict)





# (Optional) Overwrite the JSON file with filtered data
#with open(json_path, 'w') as f:
 #   json.dump(filtered_data, f, indent=4)

print(f"Filtered JSON saved. \nOriginal count: {len(data)}\nAfter filter: {len(filtered_dict)}\n Num of good cameras: {len(existing_files)}")
