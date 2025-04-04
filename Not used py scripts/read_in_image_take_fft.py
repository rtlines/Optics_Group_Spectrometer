##############################################################################
# read_in_image_take-fft.py
##############################################################################
# This script reads in an image and takes it's fourier transform
#
# It also converts the image and its fft to arrays and looks at rows in 
#   the arrays and plots them.
##############################################################################
# Author R. Todd Lines
# Last Modified:  2024-10-30
##############################################################################
# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Name of the image file to read in
image_filename = "rounded_aperture.png"

# New function to create a 2D fft of the image.  As usual, the image 
#   cordinates need to be shifted so the 0,0 position is in the middle of 
#   the image. The ifftshift command from the np fft libary does this
def calculate_2dft(input):
    ft = np.fft.ifftshift(input)
    ft = np.fft.fft2(ft)
    return np.fft.fftshift(ft)

# Read and process image.  We are only going to deal with grayscale images
#  for now so after reading hte image convert to grayscale
image = plt.imread(image_filename)
image = image[:, :, :3].mean(axis=2)  # Convert to grayscale
# and once ithe image is grayscale, make it look grayscale
plt.set_cmap("gray")

# Now compute the 2D fft of the image.
ft = calculate_2dft(image)

# try to convert the image to an array
im_array=np.array(image)

# and why not convert the fft image to an array as well
ft_array=np.array(ft)

# For plotting find the size of the array (assume a squre array!)
arr_side_length=np.shape(im_array)
print("image shape in pixels", np.shape(im_array), "should be square or you need to change the code!")
print("so the side length is ", arr_side_length[0])

# Make numbers for an x-axis that just go from zero to the side length
x=np.arange(0,arr_side_length[0],1)

# Now split out one line of the image, say, the 500th row
y=im_array[500]

# Plot the image
plt.subplot(221)
plt.imshow(image)
plt.axis("off")

# Plot the fft
plt.subplot(222)
plt.imshow(np.log(abs(ft)))

# Plot the slice of the image
plt.subplot(223)
plt.plot(x,y)

# Now plot a slice of the fft, but we want to see the details of the middle of
#  The plot so take a percentage of the data to show.
plt.subplot(224)
# Here is our slice of the fft
y=ft_array[500]

# we want to plot around the middle, so find the half way pont
half=int(arr_side_length[0]/2)
fourth=int(half/2)
eigth=int(fourth/2)
sixteenth=int(eigth)
d32=int(sixteenth/2)
d64=int(d32/2)
delta=d64

# now plot from the half way point - delta to the half way point plus delta
plt.plot(x[half-delta:half+delta],y[half-delta:half+delta])
plt.axis("off")
plt.show()