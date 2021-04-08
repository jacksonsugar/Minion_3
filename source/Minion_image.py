#!/usr/bin/env python
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import configparser
import pickle

GPIO.setwarnings(False)

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)
config = configparser.ConfigParser()
config.read(configLoc)

i = 0
light = 12
power = 32

def picture():
    try:
        # Collect time value from pickle on desktop
        firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
        samp_time = pickle.load(firstp)
        samp_count = str(len(os.listdir("{}/minion_pics/".format(configDir)))+1)
        samp_time = "{}-{}".format(samp_count, samp_time)
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
        time.sleep(10)
        camera.capture('{}/minion_pics/{}.jpg'.format(configDir, samp_time))
        time.sleep(5)
        camera.stop_preview()

    except:
        print("Camera error")
        camera.stop_preview()
        
if __name__ == '__main__':

    camera = PiCamera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light, GPIO.OUT)
    GPIO.setup(power, GPIO.OUT)
    pLED = GPIO.PWM(LED, 200)
    pLED.start(40)

    picture()

    pLED.stop()