
import os
import config
import time 

gif_delay = 50 # How much time between frames in the animated gif

tstart=time.time()

sampledir="../samplepics/"
w=1920/3
h=1080/3


graphicsmagick = "gm convert -size " + str(w) + "x" + str(h) + " -delay " + str(gif_delay) + " " + sampledir + "image*.jpg " + sampledir + "test.gif"
print graphicsmagick
os.system(graphicsmagick) #make the .gif

print "gm time :" + str(time.time() -tstart)


tstart=time.time()
imagemagick="convert -scale " + str(w) + "x" + str(h) + " -delay " + str(gif_delay) + " " + sampledir + "image*.jpg " + sampledir  + "testim.gif"

print imagemagick
os.system(imagemagick)

print "im time :" + str(time.time() - tstart)
