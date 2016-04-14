#!/usr/bin/env python

import subprocess
import time
import picamera
import config
import os
fps = 1 # delay between pics
total_pics = 4 # number of pics  to be taken
file_path = '/home/pi/photobooth/' #where do you want to save the photos

now = time.strftime("%Y%m%d%H%M%S") #get the current date and time for the start of the filename


pixel_width = 800  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
# pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 480  # 666

camera_vflip=False
camera_hflip=False

total_pics = 4 # number of pics to be taken
capture_delay = 1 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
restart_delay = 10 # how long to display finished message before beginning a new session

gif_delay = 50  # How much time between frames in the animated gif
gif_width = 640  # dimensions of the gif to be uploaded - based on the maximum size twitter allows, make integer scale factor of the image resolution for faster scaling
gif_height = 360

camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview()

try:  # take the photos
    # for i, filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
    for i in range(0, total_pics):
        # countdown(camera)
        filename = config.file_path + now + '-0' + str(i + 1) + '.jpg'
        camera.capture(filename,resize=(gif_width,gif_height))
        #GPIO.output(led2_pin, True)  # turn on the LED
        print(filename)
        time.sleep(0.25)  # pause the LED on for just a bit
        #GPIO.output(led2_pin, False)  # turn off the LED
        time.sleep(capture_delay)  # pause in-between shots
        if i == total_pics - 1:
            break
finally:
    camera.stop_preview()
    camera.close()


tstart = time.time()
# prepare the gif conversion string
graphicsmagick = "gm convert -size " + str(gif_width) + "x" + str(gif_height) + " -delay " + str(gif_delay) + " " + config.file_path + now + "*.jpg " + config.file_path + now + ".gif"
os.system(graphicsmagick) # make the .gif

print "gm time :" + str(time.time() -tstart)