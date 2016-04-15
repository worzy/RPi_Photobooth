#!/usr/bin/env python
# created by steve@stevesiden.com
# modified from chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/

import os
import glob
import time
import traceback
from time import sleep
import atexit
import RPi.GPIO as GPIO #using physical pin numbering change in future?
import picamera   # http://picamera.readthedocs.org/en/release-1.4/install2.html
import sys
import socket
import pygame #pygame for displaying images
import config
import shutil
import random #for choosing random status update
from PIL import Image, ImageDraw, ImageFont # for creating mosaics and other basic image things. use Pillow implementation
from twython import Twython # twitter library
from signal import alarm, signal, SIGALRM, SIGKILL  # stuff for the keyboard interrupt thing for the pygame

########################
### System Config ###
########################
post_online = 1  # default 1. Change to 0 if you don't want to upload pics.
backup_pics = 1  # backup pics = 1, no backup, change to 0
fullscreen = 0  # set pygame to be fullscreen or not - useful for debugging
real_path = os.path.dirname(os.path.realpath(__file__)) # path of code for references to pictures
idle_time = 10 # time in seconds to wait to idle stuff
missedfile_appendix = "-FILENOTUPLOADED" # thing added to end of file if it wasnt uploaded

########################
### Camera Config ###
########################

pixel_width = 1024  # 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
# pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 600  # 666

camera_vflip=False
camera_hflip=False

total_pics = 4 # number of pics to be taken
capture_delay = 1 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
restart_delay = 10 # how long to display finished message before beginning a new session


########################
### Gif Config ###
########################
gif_delay = 50  # How much time between frames in the animated gif
gif_width = 640  # dimensions of the gif to be uploaded - based on the maximum size twitter allows, make integer scale factor of the image resolution for faster scaling
gif_height = 360


########################
### Monitor Config ###
########################
font = ImageFont.truetype("/assets/FreeSerif.ttf", 200) #font used to overlay on pictures during countdown
monitor_w = 1024  #1024 # this is res of makibes 7" screen
monitor_h = 600  #600
transform_x = 640  #640 # how wide to scale the jpg when replaying
transform_y = 480  #480 # how high to scale the jpg when replaying
offset_x = 10  # how far off to left corner to display photos
offset_y = 0  # how far off to left corner to display photos
replay_delay = 1  # how much to wait in-between showing pics on-screen after taking
replay_cycles = 1  # how many times to show each photo on-screen after taking


########################
### Internet Config ###
########################

test_server = 'www.google.com'


#setup the twitter api client
twitter_api = Twython(
    config.twitter_CONSUMER_KEY,
    config.twitter_CONSUMER_SECRET,
    config.twitter_ACCESS_KEY,
    config.twitter_ACCESS_SECRET,
)

hashtags = "#Clarl2016"

statuses = [
    "Beep Boop! I was programmed to love!",
    "Weddings are fun! Beep Boop!",
    "Beep Boop! A memento of the day!",
    "Don't they look great!?",
    "I'm ready for my close up",
    "Smile! You're on Clarl cam!",
    "Say cheese! You're crackers!",
    "I heart Clarl!"
]


####################
### GPIO Config ####
####################
led1_pin = 16  # LED 1 #15
led2_pin = 10  # LED 2 #19
led3_pin = 21  # LED 3 #21
led4_pin = 5   # LED 4 #23
button1_pin = 23  # pin for the big red button
button2_pin = 4   # pin for printer switch
button3_pin = 17  # pin for button to end the program, but not shutdown the pi
GPIO.setmode(GPIO.BCM) # use the normal wiring numbering
GPIO.setwarnings(False) # ignore warnings if cleanup didnt run somehow
GPIO.setup(led1_pin,GPIO.OUT)  # LED 1
GPIO.setup(led2_pin,GPIO.OUT)  # LED 2
GPIO.setup(led3_pin,GPIO.OUT)  # LED 3
GPIO.setup(led4_pin,GPIO.OUT)  # LED 4
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # falling edge detection on button 1
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # falling edge detection on button 2
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # falling edge detection on button 3
GPIO.output(led1_pin,False) # set all low
GPIO.output(led2_pin,False)
GPIO.output(led3_pin,False)
GPIO.output(led4_pin,False)

#################
### Functions ###
#################


def cleanup():
    print('Ended abruptly')
    GPIO.cleanup()
    pygame.quit()
    #atexit.register(cleanup)


def shut_it_down():
    print "Shutting down..."
    #GPIO.output(led1_pin,True)
    GPIO.output(led2_pin,True)
    #GPIO.output(led3_pin,True)
    #GPIO.output(led4_pin,True)
    os.system("sudo halt")


def exit_photobooth():
    print "Photo booth app ended. RPi still running"
    #GPIO.output(led1_pin,True)
    time.sleep(3)
    raise SystemExit


def clear_pics(foo): #why is this function being passed an arguments?
    #delete files in folder on startup
    files = glob.glob(config.file_path + '*')
    for f in files:
        os.remove(f)
    #light the lights in series to show completed
    print "Deleted previous pics"
    #GPIO.output(led1_pin,False) #turn off the lights
    GPIO.output(led2_pin,False)
    #GPIO.output(led3_pin,False)
    #GPIO.output(led4_pin,False)


def is_connected():
    try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
        host = socket.gethostbyname(test_server)
    # connect to the host -- tells us if the host is actually
    # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def idle_stuff():
    connected = is_connected()

    if connected:
        print "uploading missing files"
    else:
        print "not connected :("


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


def countdown(camera):
    overlay_renderer = None
    for j in range(1,4):
        img = Image.new("RGB", (monitor_w, monitor_h))
        draw = ImageDraw.Draw(img)
        draw.text((monitor_w/2,monitor_h/2), str(4-j), (255, 255, 255), font=font)
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(img.tostring(),layer=3,size=img.size,alpha=28)
        else:
            overlay_renderer.update(img.tostring())
        sleep(1)
    img = Image.new("RGB", (monitor_w, monitor_h))
    draw = ImageDraw.Draw(img)
    draw.text((monitor_w/2,monitor_h/2), " ", (255, 255, 255), font=font)
    overlay_renderer.update(img.tostring())


def show_image(image_path):
    screen = init_pygame()
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (transform_x,transform_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()


def tweet_pics(jpg_group):
    # get filename for this gorup of photos
    now = jpg_group
    fname = config.file_path + now + '.gif'
    # choose new status from list and at the hashtags
    status_choice = random.choice(statuses)
    status_total = status_choice + " " + hashtags
    print "Tweeting: " + fname + " with status : " + status_total
    twitter_photo = open(fname, 'rb')  # open file
    response = twitter_api.upload_media(media=twitter_photo)  # upload to twitter
    # update status with image and new status
    twitter_api.update_status(media_ids=[response['media_id']], status=status_total)


## DISPLAY PICS MAKES LOADS OF PYGAMES FOR SOME REASON!
def display_pics(jpg_group):
    screen = init_pygame()
    for i in range(0, replay_cycles):  # show pics a few times
        for i in range(1, total_pics+1):  # show each pic
            filename = config.file_path + jpg_group + "-0" + str(i) + ".jpg"
            show_image(filename)
            time.sleep(replay_delay)  # pause


def pics_backup(now):
    print "Backing Up Photos" + now
    shutil.copy(config.file_path + now + '-01.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-02.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-03.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '-04.jpg', config.backup_path)
    shutil.copy(config.file_path + now + '.gif', config.backup_path)
    #shutil.copy(config.file_path  + now + '_total.jpg', config.backup_path)

# define the photo taking function for when the big button is pressed


def start_photobooth(self):

    ################################# Begin Step 1 #################################
    show_image(real_path + "/assets/blank.png")
    print "Get Ready"
    GPIO.output(led2_pin,True)
    show_image(real_path + "/assets/instructions.png")
    sleep(prep_delay)
    #GPIO.output(led2_pin,False)

    show_image(real_path + "/assets/blank.png")
    camera = picamera.PiCamera()
    camera.resolution = (pixel_width, pixel_height)
    camera.vflip = camera_vflip
    camera.hflip = camera_hflip
    camera.start_preview()

    #sleep(2) # warm up camera

    ################################# Begin Step 2 #################################
    print "Taking pics"
    now = time.strftime("%Y%m%d%H%M%S") # get the current date and time for the start of the filename
    try: # take the photos
        #for i, filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
        for i in range(0, total_pics):
            #countdown(camera)
            filename = config.file_path + now + '-0' + str(i+1) + '.jpg'
            camera.capture(filename)
            GPIO.output(led2_pin,True) # turn on the LED
            print(filename)
            sleep(0.25) # pause the LED on for just a bit
            GPIO.output(led2_pin,False) # turn off the LED
            sleep(capture_delay) # pause in-between shots
            if i == total_pics-1:
                break
    finally:
        camera.stop_preview()
        camera.close()
    ########################### Begin Step 3 #################################

    print "Creating an animated gif"
    if post_online:
        show_image(real_path + "/assets/uploading.png")
    else:
        show_image(real_path + "/assets/processing.png")
        
    GPIO.output(led2_pin,True) # turn on the LED
    # prepare the gif conversion string
    graphicsmagick = "gm convert -size " + str(gif_width) + "x" + str(gif_height) + " -delay " + str(gif_delay) + " " + config.file_path + now + "*.jpg " + config.file_path + now + ".gif"
    os.system(graphicsmagick) # make the .gif


### HERE WE NEED TO CHECK INTERNET BEFORE HAND!!!

    needtobackup = 1
    if post_online: # turn off posting pics online in the variable declarations at the top of this document
        print "Uploading to twitter Please check @ClarlPhoto soon."
        connected = is_connected() # check to see if you have an internet connection
        if not connected:
            needtobackup = 1
        while connected:
            try:
                print "We have internet. Uploading now"
                tweet_pics(now) # tweet pictures
                pics_backup(now) # backup pictures into folder
                needtobackup=0
                print "tweeting ok"
                break
            except ValueError:
                print "Oops. No internect connection. Upload later."
                needtobackup = 1

    if needtobackup:
        try:  # make a text file as a note to upload the .gif later
            file = open(config.file_path + now + "-FILENOTUPLOADED.txt",'w')   # Trying to create a new file or open one
            file.close()
        except:
            print('Something went wrong. Could not write file.')
            sys.exit(0) # quit Python



    ########################### Begin Step 4 #################################

    #GPIO.output(led4_pin,True) #turn on the LED
    try:
        display_pics(now)
    except Exception, e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)

    pygame.quit()
    print "All Photobooth stuff Done"
    GPIO.output(led4_pin,False) #turn off the LED

    
    if post_online:
        show_image(real_path + "/assets/finished_connected.png")
    else:
        show_image(real_path + "/assets/finished_offline.png")

    time.sleep(restart_delay)

    show_image(real_path + "/assets/intro.png")


########################################################################################################################

####################
### Main Program ###
####################

# add cleanup command to atexit, to ensure it runs when program stops for whatever reason
atexit.register(cleanup)

### GPIO SETUP ###

# when a falling edge is detected on button2_pin and button3_pin, regardless of whatever
# else is happening in the program, their function will be run

# Shut down Pi
#GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=shut_it_down, bouncetime=300)

# Button to close python
GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=exit_photobooth, bouncetime=300) #use third button to exit python. Good while developing

#GPIO.add_event_detect(button3_pin, GPIO.FALLING, callback=clear_pics, bouncetime=300) #use the third button to clear pics stored on the SD card from previous events

# Start Photobooth
GPIO.add_event_detect(button1_pin, GPIO.FALLING, callback=start_photobooth, bouncetime=500) #button to start photobooth

# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
    raise Exception('No suitable video driver found!')


print "Deleting old files"
# delete files in folder on startup
files = glob.glob(config.file_path + '*')
for f in files:
    os.remove(f)

print "Photo booth app running..."
#GPIO.output(led1_pin,True); # light up the lights to show the app is running
GPIO.output(led2_pin,True)
#GPIO.output(led3_pin,True);
#GPIO.output(led4_pin,True);
time.sleep(3)
#GPIO.output(led1_pin,False); # turn off the lights
GPIO.output(led2_pin,False)
#GPIO.output(led3_pin,False);
#GPIO.output(led4_pin,False);


show_image(real_path + "/assets/intro.png")

tstart = time.time()

try:
    while True:
        tcurrent = time.time()

        if (tcurrent - tstart) > idle_time:
            print "do idle stuff"
            #idle_stuff()
            tstart = tcurrent
        else:
            time.sleep(.1)

finally:
    cleanup()
    print "finally bit"

#except KeyboardInterrupt:
#    print "Interupt keyboard"
#    cleanup()

cleanup() # cleanup on normal exit

