import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# List of CSV file paths
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

# Load the CSV files into dataframes
dataframes = {path: pd.read_csv(path) for path in file_paths}

# Dictionary to map file paths to labels
file_labels = {
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv': '1M NaOH - 660 sec',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': '1M NaOH - 300 sec',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': '1M NaOH - 100 sec',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv': '1M NaCl + 1M NaOH - 660 sec',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': '1M NaCl + 1M NaOH - 300 sec',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': '1M NaCl + 1M NaOH - 100 sec',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv': '1M NaCl - 660 sec',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv': '1M NaCl - 300 sec',
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv': '1M NaCl - 100 sec'
}

# Extract total volumes from the dataframes
total_volumes = {}
for path, df in dataframes.items():
    total_volume_row = df[df['Index'] == 'Total Volume']
    if not total_volume_row.empty:
        total_volumes[path] = total_volume_row['Volume (µm^3)'].values[0]

# Extract the labels and corresponding volumes
labels = [file_labels[path] for path in total_volumes.keys()]
volumes = list(total_volumes.values())

# Define the required order based on user request
required_order = [
    '1M NaCl - 100 sec',
    '1M NaCl + 1M NaOH - 100 sec',
    '1M NaOH - 100 sec',
    '1M NaCl - 300 sec',
    '1M NaCl + 1M NaOH - 300 sec',
    '1M NaOH - 300 sec',
    '1M NaCl - 660 sec',
    '1M NaCl + 1M NaOH - 660 sec',
    '1M NaOH - 660 sec'
]

# Define colors based on time points (100, 300, 660 seconds have the same color)
colors_by_time = {
    '100 sec': 'blue',
    '300 sec': 'green',
    '660 sec': 'red'
}

# Extract colors based on the required order
colors = []
for label in required_order:
    if '100 sec' in label:
        colors.append(colors_by_time['100 sec'])
    elif '300 sec' in label:
        colors.append(colors_by_time['300 sec'])
    elif '660 sec' in label:
        colors.append(colors_by_time['660 sec'])

# Re-arrange the labels, volumes, and colors based on this new order
sorted_labels_volumes = sorted(zip(labels, volumes, colors), key=lambda x: required_order.index(x[0]))

# Unzip the sorted tuples
sorted_labels, sorted_volumes, sorted_colors = zip(*sorted_labels_volumes)

# # Plot the grouped bar chart with the correct order
# plt.figure(figsize=(12, 6))
# plt.bar(sorted_labels, sorted_volumes, color=sorted_colors)
# plt.xticks(rotation=45, ha='right')
# plt.ylabel('Total Volume (µm³)')
# plt.title('Comparison of Total Volumes (Sorted by Time and Material: 100, 300, 660 seconds)')
# plt.tight_layout()
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Define the values for each time point and material
value_NaCl = [sorted_volumes[0], sorted_volumes[3], sorted_volumes[6]]  # 1M NaCl (100, 300, 660 seconds)
value_NaCl_NaOH = [sorted_volumes[1], sorted_volumes[4], sorted_volumes[7]]  # 1M NaCl + 1M NaOH (100, 300, 660 seconds)
value_NaOH = [sorted_volumes[2], sorted_volumes[5], sorted_volumes[8]]  # 1M NaOH (100, 300, 660 seconds)

# Define the x-coordinates for the three categories (NaCl, NaCl+NaOH, NaOH)
x_1 = np.array([0, 1, 2])  # NaCl
x_2 = np.array([0.2, 1.2, 2.2])  # NaCl+NaOH
x_3 = np.array([0.4, 1.4, 2.4])  # NaOH

# # Define the categories (100 sec, 300 sec, 660 sec)
# categories = ['100 sec', '300 sec', '660 sec']
categories = ['Before Current', 'During Current', 'After Current']

# Plot the bar chart with categories for each material
plt.figure(figsize=(10, 6))
plt.bar(x_1, value_NaCl, color='r', width=0.2, label='1M NaCl', alpha=0.7)
plt.bar(x_2, value_NaCl_NaOH, color='g', width=0.2, label='1M NaCl + 1M NaOH', alpha=0.7)
plt.bar(x_3, value_NaOH, color='b', width=0.2, label='1M NaOH', alpha=0.7)

# Add legend, set x-ticks with the categories
plt.legend()
plt.xticks(x_2, categories)
plt.ylabel('Total Volume (µm³)')
plt.title('Comparison of Total Volumes by Time and Material')
plt.tight_layout()
# plt.show()
plt.savefig('../log_scale_img/total_volumes_comparison.png', dpi=300)
