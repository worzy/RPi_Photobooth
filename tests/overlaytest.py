import time
import picamera
import config
import os
import sys
import traceback
from PIL import Image, ImageDraw, ImageFont

pixel_width = 1824  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
# pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 984  # 666

camera_vflip = False
camera_hflip = False

fnt = ImageFont.truetype('FreeSerif.ttf', 400)

camera = picamera.PiCamera()
camera.resolution = (pixel_width, pixel_height)
camera.vflip = camera_vflip
camera.hflip = camera_hflip
camera.start_preview()

# Load the arbitrarily sized image
monitor_w = 1824
monitor_h = 984

countdown_seconds = 3  # time to countdown with overlay before starting 3
overlay_alpha = 28  # opacity of overlay during countdown 28


def makeoverlay(string_to_display):
    # create image size of monitor - this can be any arbitrary size
    img_orig = Image.new("RGB", (monitor_w, monitor_h))  # no inputs mean filled with black
    # create drawing object
    draw = ImageDraw.Draw(img_orig)
    # draw text in image, this should *hopefully* be in the middle of the display
    draw.text((monitor_w / 2, monitor_h / 2), string_to_display, (255, 255, 255),
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
    for j in range(1, countdown_seconds + 1):
        # create image with text located in centre - correct size
        overlay_cur = makeoverlay(str((countdown_seconds + 1) - j))
        # overlay this on screen, starting overlay if necessary
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(overlay_cur.tostring(), layer=3, size=overlay_cur.size, alpha=overlay_alpha)
        else:
            overlay_renderer.update(overlay_cur.tostring())
        time.sleep(1)

    # when this is finished, hide overlay by making it blank DO WE NEED THIS? CANT WE SET LAYER TO 2 OR REMOVE IT?
    #overlay_cur = makeoverlay("")
    #overlay_renderer.update(overlay_cur.tostring())
    camera.remove_overlay(overlay_renderer)

try:
    countdown_overlay(camera)
except Exception, e:
    tb = sys.exc_info()[2]
    traceback.print_exception(e.__class__, e, tb)

time.sleep(3)

camera.stop_preview()
camera.close()
