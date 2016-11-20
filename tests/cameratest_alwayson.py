#!/usr/bin/env python

import time
import picamera
import config
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
fps = 1 # delay between pics
total_pics = 4 # number of pics  to be taken
file_path = '/home/pi/photobooth/' #where do you want to save the photos

now = time.strftime("%Y%m%d%H%M%S") #get the current date and time for the start of the filename


pixel_width = 2592  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
pixel_height = 1944  # 666

# 2592x1944 1296x972 1296x730 640x480

# Load the arbitrarily sized image
monitor_w = 1024
monitor_h = 600

overlaytext_x = monitor_w / 2 - 100
overlaytext_y = monitor_h / 4 -50

fnt = ImageFont.truetype('FreeSerif.ttf', 400)

camera_vflip=False
camera_hflip=False

total_pics = 4 # number of pics to be taken
capture_delay = .2 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
restart_delay = 10 # how long to display finished message before beginning a new session

gif_delay = 50  # How much time between frames in the animated gif
gif_width = 640  # dimensions of the gif to be uploaded - based on the maximum size twitter allows, make integer scale factor of the image resolution for faster scaling
gif_height = 480

countdown_number = 3  # time to countdown with overlay before starting 3
countdown_time=.2
overlay_alpha = 28  # opacity of overlay during countdown 28



camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview(fullscreen=True)

try:
    while True:
        tstart = time.time()
except KeyboardInterrupt:
    print "stopping now"
    camera.stop_preview()
    camera.close()



