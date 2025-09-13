# This is a parameter file.
# Everything that needs to be changed between experiments/files should be defined here.

import os  as os

input_folder = "data"
output_folder = "plots"

# splitter: The character used to split filenames when searching for the target image suffix.
splitter = "."

# target_image_suffix: The expected suffix (filename ending, could just be the file extension) for images to be processed. 
# Only files ending with this suffix will be selected for analysis. 
target_image_suffix = "tif"

export_plots = False
plot_img = False
skeleton_length_low_threshold = 1 # For line 174-175
gap_threshold = 5 # For line 207
skeleton_length_low_threshold_after_gap = 10 # For line 222, comment out that line and plot below that if not using this parameter
