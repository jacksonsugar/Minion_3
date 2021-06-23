#!/usr/bin/env python
import os
import time
import RPi.GPIO as GPIO

wifi = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wifi, GPIO.OUT)

print('Goodbye')
GPIO.output(wifi, 0)
time.sleep(5)
os.system('sudo shutdown now')


