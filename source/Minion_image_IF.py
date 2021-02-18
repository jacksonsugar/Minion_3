#!/usr/bin/python3
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import configparser
import pickle

data_rec = 16

NumSamples = 0
samp_count = 1

light = 12
power = 32

sampNum = [0]

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(power, GPIO.OUT)

def str2bool(v):
    return v.lower() in ("yes","true",'1','t')

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)
config = configparser.ConfigParser()
config.read(configLoc)

if len(os.listdir('{}/minion_pics'.format(configDir))) == 0:

    Stime = float(config['Initial_Samples']['hours'])
    Srate = float(config['Initial_Samples']['Camera_sample_rate'])
    RECOVER = 0

    for dataNum in os.listdir('{}/minion_data/INI/'.format(configDir)):
        if dataNum.endswith('_Pic-INI.jpg'):
            sampNum.append(int(dataNum.split("-",1)[0]))

else:

    Stime = float(config['Final_Samples']['hours'])
    Srate = float(config['Final_Samples']['Camera_sample_rate'])
    RECOVER = 1

    for dataNum in os.listdir('{}/minion_data/FIN/'.format(configDir)):
        if dataNum.endswith('_Pic-FIN.jpg'):
            sampNum.append(int(dataNum.split("-",1)[0]))

samp_count = max(sampNum) + 1    

TotalSamples = Stime*(60/Srate)

def update_time():
    try:
        samp_time = os.popen("sudo hwclock -u -r").read()
        samp_time = samp_time.split('.',1)[0]
        samp_time = samp_time.replace("  ","_")
        samp_time = samp_time.replace(" ","_")
        samp_time = samp_time.replace(":","-")

        firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","wb")
        pickle.dump(samp_time, firstp)
        firstp.close()
    except:
        print("update time failed")

def picture(configDir, NumSamples, RECOVER):
    try:
        firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
        samp_time = pickle.load(firstp)

        GPIO.output(light, 1)
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
        time.sleep(10)

        if RECOVER == 0:

            samp_time = "{}-{}-{}".format(samp_count, NumSamples, samp_time)
            camera.capture('{}/minion_data/INI/{}_Pic-INI.jpg'.format(configDir, samp_time))

        else:      

            samp_time = "{}-{}-{}".format(samp_count, NumSamples, samp_time)
            camera.capture('{}/minion_data/FIN/{}_Pic-FIN.jpg'.format(configDir, samp_time))
        
        time.sleep(1)
        print("Image : {}".format(samp_time))
        camera.stop_preview()
        GPIO.output(light, 0)

    except:
        camera.stop_preview()
        GPIO.output(light, 0)
        print("Camera Error")


picture(configDir, NumSamples, RECOVER)
# Spew readings
while NumSamples <= TotalSamples:


    NumSamples = NumSamples + 1

    time.sleep(Srate*60)

    update_time()

    picture(configDir, NumSamples, RECOVER)

