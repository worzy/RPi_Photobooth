#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

countdown_led1_pin = 2  # LED 1 #15
countdown_led2_pin = 3  # LED 1 #15
countdown_led3_pin = 4  # LED 1 #15

photo_indicator_pin = 17  # LED 2 #19
processing_indicator_pin = 22  # LED 3 #21
uploading_indicator_pin = 27   # LED 4 #23


GPIO.setup(countdown_led1_pin,GPIO.OUT)
GPIO.setup(countdown_led2_pin,GPIO.OUT)
GPIO.setup(countdown_led3_pin,GPIO.OUT)
GPIO.setup(photo_indicator_pin,GPIO.OUT)
GPIO.setup(processing_indicator_pin,GPIO.OUT)
GPIO.setup(uploading_indicator_pin,GPIO.OUT)


GPIO.output(countdown_led1_pin,0)
GPIO.output(countdown_led2_pin,0)
GPIO.output(countdown_led3_pin,0)
GPIO.output(photo_indicator_pin,0)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,0)
GPIO.output(countdown_led3_pin,0)
GPIO.output(photo_indicator_pin,0)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,1)
GPIO.output(countdown_led3_pin,0)
GPIO.output(photo_indicator_pin,0)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,1)
GPIO.output(countdown_led3_pin,1)
GPIO.output(photo_indicator_pin,0)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,1)
GPIO.output(countdown_led3_pin,1)
GPIO.output(photo_indicator_pin,1)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,1)
GPIO.output(countdown_led3_pin,1)
GPIO.output(photo_indicator_pin,1)
GPIO.output(processing_indicator_pin,1)
GPIO.output(uploading_indicator_pin,0)

sleep(1)

GPIO.output(countdown_led1_pin,1)
GPIO.output(countdown_led2_pin,1)
GPIO.output(countdown_led3_pin,1)
GPIO.output(photo_indicator_pin,1)
GPIO.output(processing_indicator_pin,1)
GPIO.output(uploading_indicator_pin,1)

sleep(1)

GPIO.output(countdown_led1_pin,0)
GPIO.output(countdown_led2_pin,0)
GPIO.output(countdown_led3_pin,0)
GPIO.output(photo_indicator_pin,0)
GPIO.output(processing_indicator_pin,0)
GPIO.output(uploading_indicator_pin,0)

GPIO.cleanup()
