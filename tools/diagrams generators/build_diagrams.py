import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data from the log
folder_path = './data/sate_drone_compare/'

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = folder_path + filename
        print(file_path)
        image_data = pd.read_csv(file_path)

        # Convert to DataFrame
        df = pd.DataFrame(image_data)

        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='image', y='total_time', hue='drone_image', data=df, palette="viridis")

        # Rotate x-axis labels for readability
        plt.xticks(rotation=90)

        # Set plot labels and title
        plt.xlabel("Image")
        plt.ylabel("Time (seconds)")
        plt.title("Time Spent on Each Image for Matching (Drone Image 1 vs Drone Image 2)")

        # Display the plot
        plt.tight_layout()
        # plt.show()
        output = filename + "_comparsion.png"
        plt.savefig(output, dpi=300)
        print('Success generate: ', output)
