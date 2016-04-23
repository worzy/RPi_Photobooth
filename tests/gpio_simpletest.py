#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_1 = 2
led_2 = 3
led_3 = 4
led_4 = 17
led_5 = 27
led_6 = 22


GPIO.setup(led_1,GPIO.OUT)
GPIO.setup(led_2,GPIO.OUT)
GPIO.setup(led_3,GPIO.OUT)
GPIO.setup(led_4,GPIO.OUT)
GPIO.setup(led_5,GPIO.OUT)
GPIO.setup(led_6,GPIO.OUT)

GPIO.output(led_1,1)
GPIO.output(led_2,1)
GPIO.output(led_3,1)
GPIO.output(led_4,1)
GPIO.output(led_5,1)
GPIO.output(led_6,1)

sleep(1)

GPIO.output(led_1,0)
GPIO.output(led_2,0)
GPIO.output(led_3,0)
GPIO.output(led_4,0)
GPIO.output(led_5,0)
GPIO.output(led_6,0)

sleep(1)

GPIO.output(led_1,1)
GPIO.output(led_2,1)
GPIO.output(led_3,1)
GPIO.output(led_4,1)
GPIO.output(led_5,1)
GPIO.output(led_6,1)

sleep(1)

GPIO.output(led_1,0)
GPIO.output(led_2,0)
GPIO.output(led_3,0)
GPIO.output(led_4,0)
GPIO.output(led_5,0)
GPIO.output(led_6,0)

sleep(1)

GPIO.output(led_1,1)
GPIO.output(led_2,1)
GPIO.output(led_3,1)
GPIO.output(led_4,1)
GPIO.output(led_5,1)
GPIO.output(led_6,1)

sleep(1)

GPIO.output(led_1,0)
GPIO.output(led_2,0)
GPIO.output(led_3,0)
GPIO.output(led_4,0)
GPIO.output(led_5,0)
GPIO.output(led_6,0)

sleep(1)

GPIO.output(led_1,1)
GPIO.output(led_2,1)
GPIO.output(led_3,1)
GPIO.output(led_4,1)
GPIO.output(led_5,1)
GPIO.output(led_6,1)

sleep(1)

GPIO.output(led_1,0)
GPIO.output(led_2,0)
GPIO.output(led_3,0)
GPIO.output(led_4,0)
GPIO.output(led_5,0)
GPIO.output(led_6,0)


GPIO.cleanup()
