#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import math
import configparser
import sys
import pickle

def flash():
        j = 0
        while j <= 2:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def check_wifi():

    if "Minion_Hub" in os.popen(iwlist).read():
        status = "Connected"
        net_status = os.popen(net_cfg).read()
        if ".Minion" in net_status:
            os.system(ifswitch)
        else:
            print("You have Minions!")

    else:
        print("No WIFI found.")
        status = "Not Connected"

    print(status)
    return status

def kill_sampling(scriptNames):

    for script in scriptNames:
        os.system("sudo pkill -9 -f {}".format(script))

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

update_time()

i = 0
wifi = 22
light = 12
IO328 = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(wifi, GPIO.OUT)
GPIO.setup(IO328, GPIO.OUT)
GPIO.output(IO328, 1)
GPIO.output(wifi, 1)

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)
config = configparser.ConfigParser()
config.read(configLoc)

Ddays = int(config['Deployment_Time']['days'])
Dhours = int(config['Deployment_Time']['hours'])

Stime = config['Data_Sample']['Minion_sample_time']

try:
    float(test_string)
    Stime = float(Stime)
except:
    Stime = float(.2)

Srate = float(config['Sleep_cycle']['Minion_sleep_cycle'])
Abort = str2bool(config['Mission']['Abort'])
iniImg = str2bool(config['Sampling_scripts']['Image'])
iniP30 = str2bool(config['Sampling_scripts']['30Ba-Pres'])
iniP100 = str2bool(config['Sampling_scripts']['100Ba-Pres'])
iniTmp = str2bool(config['Sampling_scripts']['Temperature'])
iniO2  = str2bool(config['Sampling_scripts']['Oxybase'])
iniAcc = str2bool(config['Sampling_scripts']['ACC_100Hz'])

print("Days : {}".format(Ddays))
print("Hours: {}".format(Dhours))
print("Sample rate (hours) - {}".format(Srate))

TotalSamples = (((Ddays*24)+Dhours))/Srate

print("Total Cycles ------- {}".format(TotalSamples))

ifswitch = "sudo python /home/pi/Documents/Minion_tools/dhcp-switch.py"

iwlist = 'sudo iwlist wlan0 scan | grep "Minion_Hub"'

net_cfg = "ls /etc/ | grep dhcp"

ping_hub = "ping 192.168.0.1 -c 1"

ping_google = "ping google.com -c 1"

ps_test = "pgrep -a python"

scriptNames = ["TempPres.py", "Minion_image.py","Minion_image_IF.py","OXYBASE_RS232.py","ACC_100Hz.py","Extended_Sampler.py","Recovery_Sampler.py","TempPres_IF.py","OXYBASE_RS232_IF.py","ACC_100Hz_IF.py","Iridium_gps.py","Iridium_data.py"]

if __name__ == '__main__':

    if iniP30 == True or iniP100 == True:
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/TempPres.py &')

    if iniImg == True:
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/Minion_image.py &')

    if iniO2 == True:
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/OXYBASE_RS232.py &')

    if iniAcc == True:
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/ACC_100Hz.py &')

    time.sleep(5)

    while(any(x in os.popen(ps_test).read() for x in scriptNames)) == True:

    ## Check for wifi

        if check_wifi() == "Connected":
            kill_sampling(scriptNames)
            flash()
            exit(0)

        else:
            print("Sampling")
            time.sleep(Stime*30)

    print('Goodbye')
    GPIO.output(wifi, 0)
    time.sleep(5)
    os.system('sudo shutdown now')
