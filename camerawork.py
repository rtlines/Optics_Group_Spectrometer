from picamera2 import Picamera2, Preview
from time import sleep
from os import system
from datetime import datetime
from numpy import empty, shape, array2string, arange  # do we even use array to string?
from numpy import sum as npsum
import matplotlib.pyplot as plt


# Takes jpg and raw picture #############################################################################
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
filename = f'{date}_Picture.jpg'
rawfilename = f'{date}_raw_file.raw'
colfilename = f'{date}_Intensity_Graph.png'

picam2 = Picamera2() 

config = picam2.create_still_configuration(main={'size':picam2.sensor_resolution},raw={'format':'SRGGB10'})#'size':picam2.sensor_resolution
picam2.configure(config)

picam2.start()
sleep(2)

# save to 2 file types: jpeg, raw
metadata = picam2.capture_file(filename)
rawdata = picam2.capture_array('raw')

# numpy array of the image (3 dimensions) ##############################################################
array=picam2.capture_array("main")
datafile=open(f"{rawfilename}.txt","w") # create a file (from the raw img we just took)
w=shape(array)[1]#width
h=shape(array)[0]#height
channels=shape(array)[2]# it is rgb 3 numbers per pixel
print(shape(array))
pixels = npsum(array,2)# turns into black and white from summing rgb values

# write pixel data to file, starting with pixel dimensions
datafile.write(f"dimensions {w},{h}")

rawdata.tofile(rawfilename)
picam2.stop()

# Plot image using pyplot, gray color map
plt.imshow(pixels, cmap="gray")
plt.show()


# attempt to sum columns to one row ###################################################
# pixels is the array with summed rgb values

# summing the columns
col_sum = npsum(pixels, axis=0)

# graphing the summed columns
plt.plot(arange(len(col_sum)),col_sum,color='xkcd:russet')
plt.title('Summed brightness across x-axis')
plt.savefig(colfilename)
plt.show()

print('done')

#calibrate with color to find pos, find ang, etc. 

'''
##############################################################################

# read_image rotate and process.py

##############################################################################

# This script reads in an image from a spectrometer and rotates it

#   and someday will process it

#

##############################################################################

# Author R. Todd Lines

# Last Modified:  2024-11-06

##############################################################################

# Import libraries

import numpy as np

import matplotlib.pyplot as plt

from PIL import Image

 

 

# Read and process image. 

image =Image.open("./solar_spectrum.jpg")

 

#The image is crooked, so streighten it

image = image.rotate(-2.09 )

 

 

# try to convert the image to an array

im_array=np.array(image)

# We are only going to deal with the images so average over the three colors

#  This effectively makes a greyscale image

grey_array = im_array[:, :, :3].mean(axis=2)  # Convert to grayscale

 

 

# find the size of the array

arr_side_length=np.shape(im_array)

# short vertice dimension first, longer horizontal dimension second

y_max=arr_side_length[0]

x_max=arr_side_length[1]

print("image shape in pixels: ", arr_side_length[0], "columns",arr_side_length[1],"rows",arr_side_length[2], "colors")

#print(x_max,y_max)

 

# Pick a line to plot somewhere in the middle

#line_to_plot=int(arr_side_length[0]/2)

 

# Make numbers for an x-axis that just go from zero to the side length

x=np.arange(0,arr_side_length[1],1)

y=np.arange(0,arr_side_length[0],1)

 

# Now split out one line of the image, say, the 500th row

#y=grey_array[line_to_plot]

 

#Find the limits of the data

y_ave=np.zeros(y_max)

reduced_data=np.empty([1,x_max])

j=0

for i in range(y_max):

    # np array indexing is [row, column]

    y_ave[i]=np.average(grey_array[i,:])

    if y_ave[i]>5:

        j=j+1

        reduced_data  = np.r_[reduced_data,[ grey_array[i,:]]]

        #reduced_data = np.append(reduced_data, grey_array[i,:], axis=0)

 

print("number of rows with data", j)

 

   

# Since we believe we streightened our image, average the columns so we get

#  one line of data that shows our image.

spec_ave=grey_array[:, :].mean(axis=0) 

 

 

# Plot the image

plt.subplot(221)

plt.imshow(image)

plt.axis("off")

 

#plot that line of data

plt.subplot(222)

plt.plot(x,spec_ave,linewidth=0.2)

plt.axis("off")

 

#plot that which rows have data

plt.subplot(223)

plt.plot(y,y_ave,linewidth=0.2)

plt.axis("off")

 

# Plot the  reduced image

plt.subplot(224)

plt.imshow(reduced_data)

plt.axis("off")

plt.show()
'''
