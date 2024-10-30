from picamera2 import Picamera2, Preview
import time
import os
import datetime

#os.chdir('/home/optics/Pictures')

# Takes jpg and raw

filename = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.jpg')
rawfilename = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.raw')

picam2 = Picamera2()

config = picam2.create_still_configuration(main={'size':picam2.sensor_resolution},raw={'format':'SRGGB10'})
picam2.configure(config)

picam2.start()
time.sleep(2)

metadata = picam2.capture_file(filename)
rawdata = picam2.capture_array('raw')

rawdata.tofile(rawfilename)
picam2.stop()


#saves as jpg, has some extra from raw attempts \/
'''
filename = 'test.jpg' #datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.jpg')

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

camera_config = picam2.create_preview_configuration(raw={'size':picam2.sensor_resolution}) #() was blank
print(camera_config)
picam2.configure(camera_config)

picam2.start()
time.sleep(2) #how long after starting before take pic

picam2.capture_file(filename)
'''

'''
picam2 = Picamera2()
camera = Picamera2()
config = camera.create_still_configuration(main={'size':picam2.sensor_resolution},raw = {},display = None)
camera.configure(config)
#camera.set_controls({'ExposureTime':120, 'AnalogueGain':1,'ColourGains':(1.8, 1.8)}) # not sure if needed - for future ref
camera.start()

r = camera.capture_request(config)
r.save('test.dng')
print(r.get_metadata)
r.release()
'''

print('done')
#/home/optics/Pictures
