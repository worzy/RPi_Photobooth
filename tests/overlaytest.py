import time
import picamera
import config
import os
import sys
import traceback
from PIL import Image, ImageDraw, ImageFont

pixel_width = 1600  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
# pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 1200  # 666

camera_vflip = False
camera_hflip = False

fnt = ImageFont.truetype('FreeSerif.ttf', 400)

camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview()

# Load the arbitrarily sized image
monitor_w=1600
monitor_h=1200


## MAKE CREATE OVERLAY A THING HERE


def countdown(camera):
    overlay_renderer = None
    for j in range(1,4):
        img = Image.new("RGB", (monitor_w, monitor_h))
        draw = ImageDraw.Draw(img)
        draw.text((monitor_w/2,monitor_h/2), str(4-j), (255, 255, 255), font=fnt)
        pad = Image.new('RGB', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
        ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0))

        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(pad.tostring(),layer=3,size=img.size,alpha=28)
        else:
            overlay_renderer.update(pad.tostring())
        time.sleep(1)


        
    img = Image.new("RGB", (monitor_w, monitor_h))
    draw = ImageDraw.Draw(img)
    draw.text((monitor_w/2,monitor_h/2), " ", (255, 255, 255), font=fnt)
    overlay_renderer.update(img.tostring())






#img.show()


# Create an image padded to the required size with
# mode 'RGB'
#pad = Image.new('RGB', (
#    ((img.size[0] + 31) // 32) * 32,
#    ((img.size[1] + 15) // 16) * 16,
#))
# Paste the original image into the padded one
#pad.paste(img, (0, 0))


#pad.show()


# Add the overlay with the padded image as the source,
# but the original image's dimensions
#o = camera.add_overlay(pad.tostring(), size=img.size)
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
#o.alpha = 128
#o.layer = 3


try:
    countdown(camera)
except Exception, e:
    tb = sys.exc_info()[2]
    traceback.print_exception(e.__class__, e, tb)





time.sleep(3)

camera.stop_preview()
camera.close()



















