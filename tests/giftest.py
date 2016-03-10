
import os
import config
import time 

gif_delay = 50 # How much time between frames in the animated gif

tstart=time.time()

sampledir="../samplepics/"


graphicsmagick = "gm convert -size 500x333 -delay " + str(gif_delay) + " " + sampledir + "image*.jpg " + sampledir + "test.gif"
os.system(graphicsmagick) #make the .gif

print time.time() -tstart
