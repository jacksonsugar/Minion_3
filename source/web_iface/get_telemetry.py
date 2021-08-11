#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import math
import configparser
import sys
import pickle


def update_time():
    try:
        samp_time = os.popen("sudo hwclock -l -r").read()
        samp_time = samp_time.split('.',1)[0]
        samp_time = samp_time.replace("  ","_")
        samp_time = samp_time.replace(" ","_")
        samp_time = samp_time.replace(":","-")

        firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","wb")
        pickle.dump(samp_time, firstp)
        firstp.close()
    except:
        print("update time failed")
    return samp_time

def read_sampcount():
    countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","rb")
    sampcount = pickle.load(countp)
    countp.close()
    return sampcount


samp_time = update_time()

samp_time = samp_time.split('_')

samp_date = samp_time[0]

samp_hour = samp_time[1]

samp_date = samp_date.replace('-','/')

samp_hour = samp_hour.replace('-',':')

samp_time = "{} {}".format(samp_date,samp_hour)

samp_count = read_sampcount()

if samp_count == 0:
    samp_count = 0
else:
    samp_count = samp_count - 1

print("<fieldset><h3>")

print("Time:  {}<br>".format(samp_time))

print("Sample counter: {}<br>".format(samp_count))

print("</h3></fieldset>")
