#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

os.system("sudo mv /var/www/html/newconfig.txt /home/pi/Desktop/Minion_config.ini")

print("Success!")

LED = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

pLED = GPIO.PWM(LED, 200)

pLED.start(40)

time.sleep(.5)

pLED.stop()

