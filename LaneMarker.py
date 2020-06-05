#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as mtlbplot
import matplotlib.image as mpimg
import numpy as np
import cv2
mtlbplot.ion()

# Read in the image
image = mpimg.imread('image.jpg')

# Make copy of image
color_select = np.copy(image)
line_image = np.copy(image)

# Save the dimension of the image
# 0 has the height
ysize=image.shape[0]
# 1 has the width
xsize=image.shape[1]
print("Image resolution: ", xsize, "x", ysize)

# Define color threshold criteria
red_threshold = 180
green_threshold = 180
blue_threshold = 180
rgb_threshold = [red_threshold, green_threshold, blue_threshold]


# Define the vertices of a triangular mask for the given image
apex = [570,370]
left_bottom = [160, 710]
right_bottom = [1072, 710]


# Perform a linear fit (y=Ax+B) to each of the three sides of the triangle
left_side = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
right_side = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
bottom_side = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

# Mask pixels below the threshold
color_thresholds = (image[:,:,0] < rgb_threshold[0]) | (image[:,:,1] < rgb_threshold[1]) | (image[:,:,2] < rgb_threshold[2])

# Find the region inside the lines
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*left_side[0] + left_side[1])) & (YY > (XX*right_side[0] + right_side[1])) & (YY < (XX*bottom_side[0] + bottom_side[1]))
               
# Mask color and region selection
color_select[color_thresholds | ~region_thresholds] = [0, 0, 0]

# Color pixels green where both color and region selections met
line_image[~color_thresholds & region_thresholds] = [0, 255, 0]

# Display the image and show region and color selections
mtlbplot.imshow(image)
x = [left_bottom[0], right_bottom[0], apex[0], left_bottom[0]]
y = [left_bottom[1], right_bottom[1], apex[1], left_bottom[1]]
mtlbplot.plot(x, y, 'r--', lw=1)
mtlbplot.imshow(color_select)
mtlbplot.imshow(line_image)
