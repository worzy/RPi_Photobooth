from PIL import Image, ImageDraw, ImageFont
import sys

im = Image.open("overlaytext.png")

monitor_w=1920
monitor_h=1080

fnt = ImageFont.truetype('FreeSerif.ttf', 400)

img = Image.new("RGB", (monitor_w, monitor_h))
draw = ImageDraw.Draw(img)
draw.text((monitor_w / 2, monitor_h / 2), "hey", (255, 255, 255), font=fnt)

img.show()

# write to stdout
img.save("foo.png")

# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
))
# Paste the original image into the padded one
pad.paste(img, (0, 0))


pad.show()

