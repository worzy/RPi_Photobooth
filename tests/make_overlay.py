from PIL import Image, ImageDraw
import sys

im = Image.open("overlaytext.png")

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw


im.show()

# write to stdout
im.save("foo.png")