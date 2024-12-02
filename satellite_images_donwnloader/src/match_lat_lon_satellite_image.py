import load_file as load_file
import pandas as pd

relative_path = '../path.txt'
dict_name_path = load_file.get_folder_file_pair(relative_path)

csv_file_path = dict_name_path['csv_file_path']
csv_filename = dict_name_path['csv_filename']
csv_path = csv_file_path + csv_filename
print(csv_path)

# with open(csv_path, mode='r') as data:
#     reader = csv.reader(data)

df = pd.read_csv(csv_path)

# Print the DataFrame
# print(df)
# print(df['Filename'])
# print(df['Top_left_lat'])


# Prompt the user for input
input_lat = float(input("Enter latitude: "))
input_lon  = float(input("Enter longitude: "))
# Print the entered input
print(f"Your Coordinates: {input_lat}, {input_lon}")

matched = False
for idx, row in df.iterrows():
    lat_huge = row['Top_left_lat']
    lat_small = row["Bottom_right_lat"]

    long_huge = row['Bottom_right_long']
    long_small = row['Top_left_lon']
    if lat_small <= input_lat and input_lat <= lat_huge\
          and long_small <= input_lon and input_lon <= long_huge:
        matched = True
        print(row['Filename'])
        break
        
if matched is False:
    print("Not match")