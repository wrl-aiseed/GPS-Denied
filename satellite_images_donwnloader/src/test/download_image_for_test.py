import requests
import os
from PIL import Image

import sys
sys.path.insert(0, '../..')
from src.load_file import get_folder_file_pair

# URL of the PNG file you want to download
relative_path = '../../path.txt'
dict_name_path = get_folder_file_pair(relative_path)
api_key = dict_name_path['google_map_api_key']
url = "https://maps.googleapis.com/maps/api/staticmap?center=25.1347115,121.4773380&zoom=18&size=1280x1280&scale=2&maptype=satellite&key="
url += api_key

# Path to the folder where you want to save the file
save_folder = "./"  # Change this to your desired folder path

# Ensure the folder exists, if not create it
os.makedirs(save_folder, exist_ok=True)

# Get the file name from the URL (this assumes the URL contains the file name)
file_name = 'sat_image_test.png'

# Full path to where the file will be saved
file_path = os.path.join(save_folder, file_name)

# Download the PNG file
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    with open(file_path, 'wb') as f:
        f.write(response.content)  # Save the file content as binary
    print(f"PNG file downloaded successfully and saved to {file_path}")
    
    im = Image.open(save_folder + file_name)
    im.show()
else:
    print(f"Failed to download the PNG file. Status code: {response.status_code}")
