from picamera2 import Picamera2, Preview
import time

picam= Picamera2()
picam.configure(picam.create_preview_configuration())
picam.start_preview(Preview.QTGL)
picam.start()
time.sleep(30)
