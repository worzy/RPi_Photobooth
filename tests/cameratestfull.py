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


pixel_width = 800  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
pixel_height = 600  # 666

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



def makeoverlay(string_to_display):
    # create image size of monitor - this can be any arbitrary size
    img_orig = Image.new("RGB", (monitor_w, monitor_h))  # no inputs mean filled with black
    # create drawing object
    draw = ImageDraw.Draw(img_orig)
    # draw text in image, this should *hopefully* be in the middle of the display
    draw.text((overlaytext_x, overlaytext_y), string_to_display, (255, 255, 255),
              font=fnt)  # text is white using font defined above
    # pad the image into the allowed buffer size of multiples of 32 * 16
    img_padded = Image.new('RGB', (
        ((img_orig.size[0] + 31) // 32) * 32,
        ((img_orig.size[1] + 15) // 16) * 16,
    ))
    # Paste the original image into the padded one
    img_padded.paste(img_orig, (0, 0))
    return img_padded


def countdown_overlay(camera):
    # display countdown as overlay on preview

    # start with no overlay
    overlay_renderer = None

    # loop through countdown values (3,2,1) displaying text
    for j in range(1, countdown_number + 1):
        # create image with text located in centre - correct size
        overlay_cur = makeoverlay(str((countdown_number + 1) - j))
        # overlay this on screen, starting overlay if necessary
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(overlay_cur.tostring(), layer=3, size=overlay_cur.size, alpha=overlay_alpha)
        else:
            overlay_renderer.update(overlay_cur.tostring())
        time.sleep(countdown_time)

    # when this is finished, hide overlay by making it blank DO WE NEED THIS? CANT WE SET LAYER TO 2 OR REMOVE IT?
    #overlay_cur = makeoverlay("")
    #overlay_renderer.update(overlay_cur.tostring())
    camera.remove_overlay(overlay_renderer)


def pics_backup(now):
    # copy the pictures into the backup folder
    print "Backing Up Photos " + now
    shutil.copy(config.file_path + now + '-01.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-02.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-03.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-04.jpg', config.backup_path)
    #shutil.copy(config.file_path + now + '.gif', config.backup_path)
    #shutil.copy(config.file_path  + now + '_total.jpg', config.backup_path)

def gif_backup(now):
    print "Backing Up gif " + now
    shutil.copy(config.file_path + now + '.gif', config.backup_path)


camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview()

try:  # take the photos
    # for i, filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
    for i in range(0, total_pics):
        countdown_overlay(camera)
        filename = config.file_path + now + '-0' + str(i + 1) + '.jpg'
        camera.capture(filename,resize=(gif_width,gif_height))
        #GPIO.output(led2_pin, True)  # turn on the LED
        print(filename)
        time.sleep(0.1)  # pause the LED on for just a bit
        #GPIO.output(led2_pin, False)  # turn off the LED
        time.sleep(capture_delay)  # pause in-between shots
        if i == total_pics - 1:
            break
finally:
    camera.stop_preview()
    camera.close()

tstart = time.time()

pics_backup(now)

print "backup time :" + str(time.time() -tstart)

# prepare the gif conversion string
graphicsmagick = "gm convert -size " + str(gif_width) + "x" + str(gif_height) + " -delay " + str(gif_delay) + " " + config.file_path + now + "*.jpg " + config.file_path + now + ".gif"
os.system(graphicsmagick) # make the .gif

print "gm time :" + str(time.time() -tstart)

gif_backup(now)

print "total time :" + str(time.time() -tstart)

