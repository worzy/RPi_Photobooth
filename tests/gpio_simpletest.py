#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led =4

GPIO.setup(led,GPIO.OUT)

GPIO.output(led,1)

sleep(1)

GPIO.output(led,0)

sleep(1)

GPIO.output(led,1)

sleep(1)

GPIO.output(led,0)


GPIO.cleanup()
