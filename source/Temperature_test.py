#!/usr/bin/python3
import RPi.GPIO as GPIO
import tsys01
import ms5837
from kellerLD import KellerLD
import time
import os
import configparser
import pickle

NumSamples = 0

samp_count = 1

def str2bool(v):
    return v.lower() in ("yes","true",'1','t')

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']

config = configparser.ConfigParser()
configLoc = '{}/Minion_config.ini'.format(configDir)

config.read(configLoc)

iniTmp = str2bool(config['Sampling_scripts']['Temperature'])

if iniTmp == True:

    sensor_temp = tsys01.TSYS01()

    # We must initialize the sensor before reading it
    if not sensor_temp.init():
        print("Error initializing Temperature sensor")
        exit(1)

    if not sensor_temp.read():
        print("Error reading sensor")
        iniTmp = False
        exit(1)

    temp = round(sensor_temp.temperature(), 4)

    print(temp)

else:

    print("Temp sensor not enabled")
