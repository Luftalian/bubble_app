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

# Define a function to plot combined histograms for the given timepoint
def plot_combined_volume_distribution_for_timepoints(dataframes, min_volume, max_volume, timepoint, files, labels, colors):
    bins = np.logspace(np.log10(min_volume), np.log10(max_volume), 30)  # Logarithmic bins

    # Create a combined histogram plot
    plt.figure(figsize=(10, 6))
    ax = plt.gca()  # Get current axis
    ax.set_axisbelow(True)  # Set grid behind data
    for file, label, color in zip(files, labels, colors):
        df_cleaned = dataframes[file][dataframes[file]['Index'] != 'Total Volume']
        plt.hist(df_cleaned['Volume (µm^3)'], bins=bins, alpha=0.6, label=label, edgecolor='black', color=color)

    plt.xscale('log')  # Set x-axis to log scale
    plt.xlabel('Volume (µm³) [Log Scale]', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.ylim(0, 92)  # Set y-axis limit from 0 to 35
    plt.xlim(min_volume, max_volume)

    # Set x-axis ticks
    xticks = np.logspace(np.log10(min_volume), np.log10(max_volume), num=10)
    plt.xticks(xticks, labels=[f"{x:.1e}" for x in xticks])

    # plt.grid(True, which='both')  # Enable grid
    plt.legend()  # Add a legend to distinguish the datasets

    # Show the combined plot
    plt.title(f'Combined Distribution of Particle Volume (µm³) at {timepoint} seconds', fontsize=14)
    # plt.show()
    # plt.savefig(f'../log_scale_img/combined_distribution_at_{timepoint}_seconds.png', dpi=300)
    plt.savefig(f'../log_scale_img/combined_distribution_at_{timepoint}_seconds_no_grid.png', dpi=300)

# Define the files and labels for 100 seconds
files_100_seconds = [
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv'
]
labels_100_seconds = ['1M NaCl', '1M NaOH', '1M NaCl + 1M NaOH']
colors_100_seconds = ['red', 'blue', 'green']

# Define the files and labels for 300 seconds
files_300_seconds = [
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv'
]
labels_300_seconds = ['1M NaCl', '1M NaOH', '1M NaCl + 1M NaOH']
colors_300_seconds = ['red', 'blue', 'green']

# Define the files and labels for 660 seconds
files_660_seconds = [
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv'
]
labels_660_seconds = ['1M NaCl', '1M NaOH', '1M NaCl + 1M NaOH']
colors_660_seconds = ['red', 'blue', 'green']

# Calculate the overall min and max volumes
all_volumes = pd.concat([df[df['Index'] != 'Total Volume']['Volume (µm^3)'] for df in dataframes.values()])
all_volumes = pd.to_numeric(all_volumes, errors='coerce')  # Convert to numeric
min_volume = all_volumes.min()
max_volume = all_volumes.max()

# Generate the combined histograms for 100, 300, and 660 seconds
plot_combined_volume_distribution_for_timepoints(dataframes, min_volume, max_volume, 100, files_100_seconds, labels_100_seconds, colors_100_seconds)
plot_combined_volume_distribution_for_timepoints(dataframes, min_volume, max_volume, 300, files_300_seconds, labels_300_seconds, colors_300_seconds)
plot_combined_volume_distribution_for_timepoints(dataframes, min_volume, max_volume, 660, files_660_seconds, labels_660_seconds, colors_660_seconds)
