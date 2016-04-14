import time
import picamera
import config
import os
from PIL import Image, ImageDraw

pixel_width = 1296  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
# pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 972  # 666

camera_vflip = False
camera_hflip = False

camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview()

# Load the arbitrarily sized image
monitor_w=640
monitor_h=480

fnt = ImageFont.truetype('FreeSerif.ttf', 100)

img = Image.new("RGB", (monitor_w, monitor_h))
draw = ImageDraw.Draw(img)
draw.text((monitor_w / 2, monitor_h / 2), "hey", (255, 255, 255), font=fnt)

img.show()


# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
))
# Paste the original image into the padded one
pad.paste(img, (0, 0))


pad.show()


# Add the overlay with the padded image as the source,
# but the original image's dimensions
o = camera.add_overlay(pad.tostring(), size=img.size)
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
o.alpha = 128
o.layer = 3


time.sleep(3)

camera.stop_preview()
camera.close()
