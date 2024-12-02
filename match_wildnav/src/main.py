"""Core module. Contains the main functions for the project."""
import cv2
import support_tools.load_file as LoadFile
import superglue_utils
import tools_data.data_write_read_csv_file as DataWriteReadCsvFile



import time
############################################################################################################
# Important variables
############################################################################################################

relative_path = './path.txt'
dict_name_path = LoadFile.get_folder_file_pair(relative_path)

map_path = dict_name_path['satellite_folder_path']
map_filename = map_path + dict_name_path['satellite_csv']
drone_photos_filename = dict_name_path['drone_folder_path'] + dict_name_path['drone_csv']
#######################################
# MAIN
#######################################


# Read the georeference consisting of satellite images 
geo_images_list = DataWriteReadCsvFile.csv_read_sat_map(map_filename)

latitude_truth = []
longitude_truth = []
latitude_calculated = []
longitude_calculated = []

# Record the start time
start_time = time.time()

# for i in range(0, 1000):
#     # print(i)
#     j = i
# Load the drone image
# TODO: Drone Image Capture from Drone
# drone_images_list = ['input.png']
drone_images_list = DataWriteReadCsvFile.csv_read_drone_images(drone_photos_filename) 
# print(str(len(drone_images_list)) + " drone photos were loaded.")

# Iterate through all the drone images
for drone_image in drone_images_list:
    # latitude_truth.append(drone_image.latitude) # ground truth from drone image metadata for later comparison
    # longitude_truth.append(drone_image.longitude) # ground truth for later comparison
    photo =  cv2.imread(drone_image.filename) # read the drone image

    max_features = 0 # keep track of the best match, more features = better match
    located = False # flag to indicate if the drone image was located in the map
    center = None # center of the drone image in the map

    #Call superglue wrapper function to match the query image to the map
    satellite_map_index_new, center_new, located_image_new, features_mean_new, query_image_new, feature_number = superglue_utils.match_image()
    # print('End')

    # If the drone image was located in the map and the number of features is greater than the previous best match, 
    #   then update the best match                                                                                                                              spective transform exceeds 1, discard the resuls in that case
    if (feature_number > max_features and center_new[0] < 1 and center_new[1] < 1):
        satellite_map_index = satellite_map_index_new
        center = center_new
        located_image = located_image_new
        features_mean = features_mean_new
        query_image = query_image_new
        max_features = feature_number
        located = True
        print(satellite_map_index)

    print(center)
    photo_name = drone_image.filename.split("/")[-1]
    # photo_name = drone_image

    # If the drone image was located in the map, calculate the geographical location of the drone image
    if center != None and located:        
        current_location = DataWriteReadCsvFile.calculate_geo_pose(geo_images_list[satellite_map_index], center, features_mean, query_image.shape )
        
        # Write the results to the image result file with the best match
        # cv2.putText(located_image, "Calculated: " + str(current_location), org = (10,625),fontFace =  cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.8,  color = (0, 0, 0))
        # cv2.putText(located_image, "Ground truth: " + str(drone_image.latitude) + ", " + str(drone_image.longitude), org = (10,655),fontFace =  cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.8,  color = (0, 0, 0))
        # cv2.imwrite(dict_name_path['results_folder_path'] + photo_name + "_located.png", located_image)
        
        print("Image " + str(photo_name) + " was successfully located in the map")
        print("Calculated location: ", str(current_location[0:2]))



        # print("Ground Truth: ", drone_image.latitude, drone_image.longitude)   
        
        # Save the calculated location for later comparison with the ground truth
        # drone_image.matched = True
        # drone_image.latitude_calculated = current_location[0]
        # drone_image.longitude_calculated = current_location[1]
        
        # latitude_calculated.append(drone_image.latitude_calculated)
        # longitude_calculated.append(drone_image.longitude_calculated)

        # print(f'satellite_map_index: {satellite_map_index}, center: {center}, located_image: {located_image},\
        #        features_mean: {features_mean}, query_image: {query_image},max_features: {max_features}')        
        
        
        
        
        
    else:
        print("NOT MATCHED:", photo_name)


# Record the end time
end_time = time.time()


# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")