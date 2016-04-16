#!/usr/bin/env python

import time
import pygame
import sys
import traceback

now = "../samplepics/image"
total_pics = 4 # number of pics  to be taken
monitor_w = 800
monitor_h = 450
transform_x = 600 #how wide to scale the jpg when replaying
transfrom_y = 450 #how high to scale the jpg when replaying
offset_x = 100 #how far off to left corner to display photos
offset_y = 0 #how far off to left corner to display photos
replay_delay = .1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 1 # how many times to show each photo on-screen after taking

fullscreen = 0


def init_pygame():
    pygame.init()  # start the pygame instance
    # set screen size
    if fullscreen:
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    else:
        size = [monitor_w, monitor_h]
    # more pygame setup
    pygame.display.set_caption('Photo Booth Pics')
    pygame.mouse.set_visible(False)  # hide the mouse cursor
    # return the pygame object with correct size
    if fullscreen:
        return pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(size)


def show_image(img_fname):
    screen=init_pygame()
    img = pygame.image.load(img_fname)
    img = pygame.transform.scale(img, (transform_x, transfrom_y))
    screen.blit(img, (offset_x, offset_y))
    pygame.display.flip()  # update the display


def display_pics(jpg_group):
    for i in range(0, replay_cycles): #show pics a few times
        for i in range(1, total_pics+1): #show each pic
            filename = jpg_group + "0" + str(i) + ".jpg"
            show_image(filename)
            time.sleep(replay_delay) # pause
try:
    display_pics(now)
except Exception, e:
    tb = sys.exc_info()[2]
    traceback.print_exception(e.__class__, e, tb)
pygame.quit()
