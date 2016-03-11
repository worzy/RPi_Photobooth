#!/usr/bin/env python

import time
import pygame
import sys
import traceback

now = "../samplepics/image"
total_pics = 4 # number of pics  to be taken
w = 800
h = 450
transform_x = 600 #how wide to scale the jpg when replaying
transfrom_y = 450 #how high to scale the jpg when replaying
offset_x = 100 #how far off to left corner to display photos
offset_y = 0 #how far off to left corner to display photos
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 4 # how many times to show each photo on-screen after taking

def display_pics(jpg_group):
    # this section is an unbelievable nasty hack - for some reason Pygame
    # needs a keyboardinterrupt to initialise in some limited circs (second time running)

    pygame.init()
    screen = pygame.display.set_mode((w,h)) 
    pygame.display.set_caption('Photo Booth Pics')
    pygame.mouse.set_visible(False) #hide the mouse cursor	
    for i in range(0, replay_cycles): #show pics a few times
        for i in range(1, total_pics+1): #show each pic
            filename = jpg_group + "0" + str(i) + ".jpg"
            print filename
            img=pygame.image.load(filename) 
            img = pygame.transform.scale(img,(transform_x,transfrom_y))
            screen.blit(img,(offset_x,offset_y))
            pygame.display.flip() # update the display
            time.sleep(replay_delay) # pause 	
	
try:
    display_pics(now)
except Exception, e:
    tb = sys.exc_info()[2]
    traceback.print_exception(e.__class__, e, tb)
pygame.quit()
