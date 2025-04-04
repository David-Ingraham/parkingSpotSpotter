import json
import os


def swap_spaces_for_unsersc():
    input_file = '../camera_id_lat_lng.json'
    output_file = 'cleaned_json.json'
    def reformat_key(key):
        street_part = key.split(',')[0]
        return street_part.replace(' @ ', '_').replace(' ', '_').replace('@', '_')

    with open(input_file, 'r') as f:
        data = json.load(f)

    reformatted_data = {reformat_key(k): v for k, v in data.items()}

    with open(output_file, 'w') as f:
        json.dump(reformatted_data, f, indent=2)

    print(f"Reformatted JSON saved to {output_file}")



def periodRemover():
    file_path = 'cleaned_json.json'

    with open(file_path,'r') as f:
        data = json.load(f)

    _json = {k.replace('.', '_'): v for k, v in data.items()}

    with open(file_path, 'w') as f:
        json.dump(_json, f, indent=2)

def doulbeRemoverFrome_json():
    file_path = 'cleaned_json.json'

    with open(file_path,'r') as f:
        data = json.load(f)

    _json = {k.replace('__', '_'): v for k, v in data.items()}

    with open(file_path, 'w') as f:
        json.dump(_json, f, indent=2)



def backslashRemoverFromjson():
    file_path = 'cleaned_json.json'

    with open(file_path,'r') as f:
        data = json.load(f)

    _json = {k.replace('/', '_'): v for k, v in data.items()}

    with open(file_path, 'w') as f:
        json.dump(_json, f, indent=2)



def doubleUnderscoreRemover():
    # Set the path to your folder
    folder_path = '../traffic_camera_images'  # change this to your actual path

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if '__' in filename:
            new_filename = filename.replace('__', '_')
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} → {new_filename}')




def removebadCameras():
    json_path = 'cleaned_file.json'  # JSON file with underscore keys
    folder_path = '../traffic_camera_images'    # Folder containing your files

    # Load the JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Get list of filenames in the folder (without extension if needed)
    filenames = set(os.listdir(folder_path))

    # If you want to match just the base names (without extensions), uncomment this:
    filenames = {os.path.splitext(name)[0] for name in filenames}

    # Filter the JSON to keep only keys that are found in the filenames
    filtered_data = {key: value for key, value in data.items() if key in filenames}

    # Save the filtered JSON
    with open('filtered_file.json', 'w') as f:
        json.dump(filtered_data, f, indent=2)

    print("Filtered JSON saved to 'filtered_file.json'")



def  main():

    #swap_spaces_for_unsersc()

    #doubleUnderscoreRemover()

    periodRemover()

    doulbeRemoverFrome_json()
    backslashRemoverFromjson()

    #removebadCameras()


if __name__ == "__main__":
    main()