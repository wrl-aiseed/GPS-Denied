import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data from the log
folder_path = './data/visual_local/'

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = folder_path + filename
        print(file_path)
        image_data = pd.read_csv(file_path)

        # Convert to DataFrame
        df = pd.DataFrame(image_data)
        print(df)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['Index'], df['Processing Time (seconds)'], marker='o', linestyle='-', color='b')
        # Rotate x-axis labels for readability
        plt.xticks(rotation=90)

        # Set plot labels and title
        plt.xlabel("Index", fontsize=12)
        plt.ylabel("Processing Time (seconds)", fontsize=12)
        plt.title("Processing Time per Index", fontsize=16)

        # Display the plot
        plt.tight_layout()
        plt.grid(True)
        # plt.show()
        output = filename + "_comparsion.png"
        plt.savefig(output, dpi=300)
        print('Success generate: ', output)
