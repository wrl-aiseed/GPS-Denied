import sys
import csv
import cv2
import haversine as hs
from haversine import Unit

from tools_data.geo_photo_drone import GeoPhotoDrone
from tools_data.geo_photo_sate import GeoPhotoSate
sys.path.insert(0, '..')
from support_tools.load_file import get_folder_file_pair

relative_path = 'path.txt'
dict_name_path = get_folder_file_pair(relative_path)

def csv_read_drone_images(filename):
    """
        Builds a list with drone geo tagged photos by reading a csv file with this format:
        Filename, Top_left_lat,Top_left_lon,Bottom_right_lat,Bottom_right_long
        "photo_name.png",60.506787,22.311631,60.501037,22.324467
    """
    geo_list_drone = []
    # photo_path = "../assets/query/"
    drone_image_path = dict_name_path['drone_folder_path']
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                
                #img = cv2.imread(photo_path + row[0],0)
                # print("Read Drone Image: ", drone_image_path + row[0])
                geo_photo = GeoPhotoDrone(drone_image_path + row[0], 0, float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]))
                geo_list_drone.append(geo_photo)
                line_count += 1

        # print(f'Processed {line_count} lines.')
        return geo_list_drone

def csv_read_sat_map(filename):
    """
        Builds a list with satellite geo tagged photos by reading a csv file with this format:
        Filename, Top_left_lat,Top_left_lon,Bottom_right_lat,Bottom_right_long
        "photo_name.png",60.506787,22.311631,60.501037,22.324467
    """
    geo_list = []
    satellite_image_path = dict_name_path['satellite_folder_path']
    print("opening: ",filename)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:      
                print("ROW: ", row)      
                img = cv2.imread(satellite_image_path + row[0],0)
                geo_photo = GeoPhotoSate(satellite_image_path + row[0],img,(float(row[1]),float(row[2])), (float(row[3]), float(row[4])))
                geo_list.append(geo_photo)
                line_count += 1

        print(f'Processed {line_count} lines.')
        geo_list.sort() # sort alphabetically by filename to ensure that the feature matcher return the right index of the matched sat image
        return geo_list
    
# def csv_write_image_location(photo):
#     header = ['Filename', 'Latitude', 'Longitude', 'Calculated_Latitude', 'Calculated_Longitude', 'Latitude_Error', 'Longitude_Error', 'Meters_Error', 'Corrected', 'Matched']
#     with open(dict_name_path['results_folder_path'] + dict_name_path['results_csv'], 'a', encoding='UTF8') as f:
#         writer = csv.writer(f)        
#         photo_name = photo.filename.split("/")[-1]
#         loc1 = ( photo.latitude, photo.longitude)
#         loc2 = ( photo.latitude_calculated, photo.longitude_calculated)
#         dist_error =  hs.haversine(loc1,loc2,unit=Unit.METERS)
#         lat_error = photo.latitude - photo.latitude_calculated
#         lon_error = photo.longitude - photo.longitude_calculated
#         line = [photo_name, str(photo.latitude), str(photo.longitude), str(photo.latitude_calculated), str(photo.longitude_calculated), str(lat_error), str(lon_error), str(dist_error), str(drone_image.corrected), str(drone_image.matched), str(drone_image.gimball_yaw + drone_image.flight_yaw - 15)]
#         writer.writerow(line)


def calculate_geo_pose(geo_photo, center, features_mean,  shape):
    """
        Calculates the geographical location of the drone image.
        Input: satellite geotagged image, relative pixel center of the drone image, 
        (center with x = 0.5 and y = 0.5 means the located features are in the middle of the sat image)
        pixel coordinatess (horizontal and vertical) of where the features are localted in the sat image, shape of the sat image
    """
    #use ratio here instead of pixels because image is reshaped in superglue    
    latitude = geo_photo.top_left_coord[0] + abs( center[1])  * ( geo_photo.bottom_right_coord[0] - geo_photo.top_left_coord[0])
    longitude = geo_photo.top_left_coord[1] + abs(center[0])  * ( geo_photo.bottom_right_coord[1] - geo_photo.top_left_coord[1])
    
    return latitude, longitude