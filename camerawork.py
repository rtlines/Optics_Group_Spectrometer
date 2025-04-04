from picamera2 import Picamera2, Preview
from time import sleep
from os import system, makedirs
from datetime import datetime
from numpy import empty, shape, arange
from numpy import sum as npsum
import matplotlib.pyplot as plt

saveName=input("Gas Name (i.e. Neon): ")
reason = input('Reason for taking this image: ')
# Takes jpg and raw picture #############################################################################
# names for all the files, folders for the files
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
filename = f'{date}_Picture.jpg' # tool out _{saveName}
#rawfilename = f'{date}_raw_file.raw'
colfilename = f'{date}_{saveName}_Intensity_Graph.png'
makedirs(saveName, exist_ok=True) # makes sure folder exists to store everything
makedirs(f'{saveName}/color_photos', exist_ok=True) # checks for Gas/color_photos folder
makedirs(f'{saveName}/spectra_plots', exist_ok=True) # checks for Gas/spectra_plots folder

picam2 = Picamera2() 

config = picam2.create_still_configuration(main={'size':picam2.sensor_resolution},raw={'format':'SRGGB10'})#'size':picam2.sensor_resolution
picam2.configure(config)

picam2.start()
sleep(2)

# save to 2 file types: jpeg, raw
metadata = picam2.capture_file(f'{saveName}/color_photos/{filename}') # saving the picture to the color_photos folder
rawdata = picam2.capture_array('raw')

# numpy array of the image (3 dimensions) ##############################################################
array=picam2.capture_array("main")
#datafile=open(f"{rawfilename}.txt","w") # create a file (from the raw img we just took)
w=shape(array)[1]#width
h=shape(array)[0]#height
channels=shape(array)[2]# it is rgb 3 numbers per pixel
print(shape(array))
pixels = npsum(array,2)# turns into black and white from summing rgb values

# write pixel data to file, starting with pixel dimensions
#datafile.write(f"dimensions {w},{h}")

#rawdata.tofile(rawfilename)
picam2.stop()


# sum columns to one row ###################################################
# pixels is the array with summed rgb values

# summing the columns
# adjusting column heights (chopping off the messy top and bottom)

t = 4 # (100/n)% how far to cut off?
b = 4
num_o_rows = pixels.shape[0] # finding out how many rows are in the array so I can
                             # chop off however much I need to
start_row = num_o_rows // t  # how many rows / n, rounded down to nearest whole num
                             # the top has been nice so far, so moving crop upwards instead of around center
                             # this cuts off top about (1/n)*100%
end_row = num_o_rows - (num_o_rows // b)  # cuts off bottom (1/n)*100%
                             # need to adjust when stuff stops moving around
mid_pixels = pixels[start_row:end_row,:] # grabs just what's between start and end row

col_sum = npsum(mid_pixels, axis=0)


'''
# uncomment when aligning stuff
plt.imsave(f'{date}_{saveName}_Cropped_Picture.jpg', mid_pixels, cmap = 'gray') # saving the cropped image
'''
# graphing the summed columns
plt.plot(arange(len(col_sum)),col_sum,color='xkcd:russet')
plt.title(f'{saveName} brightness across x-axis')
plt.savefig(f'{saveName}/spectra_plots/{filename}') # saving the intensity graph
# plt.show() # then show it

#calibrate with color to find pos, find ang, etc. 

# Write information to log folder #################################################
logfile = open(f'{saveName}/Log', 'a')
logfile.write(f'{date}\n{reason}\n\n')
logfile.close()

# Show croppedh
# Plot cropped image using pyplot, gray color map
plt.imshow(mid_pixels, cmap="gray")
plt.title('Cropped image - the values that will get summed')
plt.show()


print('done')


