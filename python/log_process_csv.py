import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load all CSV files into dataframes (this assumes the files are already loaded)
file_paths = [
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv'
]

# CSVファイルに対応するグラフタイトルを辞書で指定
titles = {
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaOH at after current',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaOH at current on',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaOH at no current',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl and 1M NaOH at after current',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl and 1M NaOH at current on',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl and 1M NaOH at no current',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl at after current',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl at current on',
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Radius (µm) - 1M NaCl at no current'
}

# Load the CSV files into dataframes
dataframes = {path: pd.read_csv(path) for path in file_paths}

# Combine all Radius (µm) data from the different dataframes to find the overall min and max
all_radii = pd.concat([df[df['Index'] != 'Total Volume']['Radius (µm)'] for df in dataframes.values()])
all_radii = pd.to_numeric(all_radii, errors='coerce')  # Convert to numeric to avoid issues
min_radius = all_radii.min()
max_radius = all_radii.max()
# 1個目がおおきすぎるから
# second_max_radius = all_radii.nlargest(2).iloc[-1]
# max_radius = second_max_radius
print(min_radius, max_radius)

# Modify the function to use a log scale for the x-axis and more ticks
def plot_radius_distribution_with_log_scale(dataframes, min_radius, max_radius):
    bins = np.logspace(np.log10(min_radius), np.log10(max_radius), 30)  # Logarithmic bins
    for file, df in dataframes.items():
        # Remove the total volume row
        df_cleaned = df[df['Index'] != 'Total Volume']

        # Create a histogram for the radius distribution with log scale
        plt.figure(figsize=(10, 6))
        plt.hist(df_cleaned['Radius (µm)'], bins=bins, edgecolor='black', alpha=0.7)
        plt.xscale('log')  # Set x-axis to log scale
        plt.title(titles[file], fontsize=14)
        plt.xlabel('Radius (µm) [Log Scale]', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.ylim(0, 80)  # Set y-axis limit from 0 to 20
        plt.xlim(min_radius, 100)

        # Set more ticks on the x-axis
        xticks = np.logspace(np.log10(min_radius), 2, num=10)  # Set ticks from min_radius to 100
        # xtickes to int
        xticks = [int(x) for x in xticks]
        plt.xticks(xticks, labels=[f"{x:.1f}" for x in xticks])

        plt.grid(True, which='both')  # Grid for both major and minor ticks

        # Save the figure instead of showing it
        output_image_path = f"../log_scale_img/output_with_log_scale_radius_{file.split('/')[-1]}.png"
        plt.savefig(output_image_path)
        plt.close()

# Generate the updated plots with log scale and consistent bins
plot_radius_distribution_with_log_scale(dataframes, min_radius, max_radius)

