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

def check_wifi(IgnoreStatus):

    networks = os.popen(iwlist).read()

    if "Master_Hub" in networks:
        print("Bypassing WIFI Lock")
        status = "Connected"

    elif "Minion_Hub" in networks and IgnoreStatus == False:
        status = "Connected"

    else:
        print("No WIFI found.")
        status = "Not Connected"

    if status == "Connected":
        net_status = os.popen(net_cfg).read()
        if ".Minion" in net_status:
            os.system(ifswitch)
        else:
            print("You have Minions!")

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
    return samp_time

def read_sampcount():
    countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","rb")
    sampcount = pickle.load(countp)
    countp.close()
    return sampcount

def update_sampcount():
    countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","rb")
    sampcount = pickle.load(countp)
    sampcount = sampcount + 1
    countp.close()
    countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","wb")
    pickle.dump(sampcount, countp)
    countp.close()
    return sampcount

samp_time = update_time()

samp_count = read_sampcount()

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


INIsamp = float(config['Initial_Samples']['hours'])
IG_WIFI_D = float(config['Mission']['Ignore_WIFI-days'])
IG_WIFI_H = float(config['Mission']['Ignore_WIFI-hours'])

IG_WIFI_Samples = (((IG_WIFI_D*24) + IG_WIFI_H)/Srate) - (INIsamp/Srate)

print("Minion Deployment Handler")
print("Time:  {}".format(samp_time))
print("Days : {}".format(Ddays))
print("Hours: {}".format(Dhours))
print("Sample rate (hours) - {}".format(Srate))

TotalSamples = (((Ddays*24)+Dhours))/Srate

if samp_count >= TotalSamples:
    RemainSamples = 0
else:
    RemainSamples = (TotalSamples - samp_count)

print("Total Cycles ------- {}".format(TotalSamples))

print("Cycles Remaining --- {}".format(RemainSamples))

if IG_WIFI_Samples >= samp_count:
    IgnoreWIFI = True
    print("Ignoring Wifi, in Mission")

else:
    IgnoreWIFI = False
    print("Searching for WIFI")

ifswitch = "sudo python /home/pi/Documents/Minion_tools/dhcp-switch.py"

iwlist = 'sudo iwlist wlan0 scan | grep -e "Minion_Hub" -e "Master_Hub"'

net_cfg = "ls /etc/ | grep dhcp"

ping_hub = "ping 192.168.0.1 -c 1"

ping_google = "ping google.com -c 1"

ps_test = "pgrep -a python"

scriptNames = ["TempPres.py", "Minion_image.py","Minion_image_IF.py","OXYBASE_RS232.py","ACC_100Hz.py","Extended_Sampler.py","Recovery_Sampler_Burn.py","TempPres_IF.py","OXYBASE_RS232_IF.py","ACC_100Hz_IF.py","Iridium_gps.py","Iridium_data.py"]

if __name__ == '__main__':

    if samp_count == 0:
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/Extended_Sampler.py &')

    elif samp_count >= TotalSamples + 1 or Abort == True:
        GPIO.output(IO328, 0)
        os.system('sudo python3 /home/pi/Documents/Minion_scripts/Recovery_Sampler_Burn.py &')

    else:
        if iniImg == True:
            os.system('sudo python3 /home/pi/Documents/Minion_scripts/Minion_image.py &')

        if iniP30 == True or iniP100 == True or iniTmp == True:
            os.system('sudo python3 /home/pi/Documents/Minion_scripts/TempPres.py &')

        if iniO2 == True:
            os.system('sudo python3 /home/pi/Documents/Minion_scripts/OXYBASE_RS232.py &')

        if iniAcc == True:
            os.system('sudo python3 /home/pi/Documents/Minion_scripts/ACC_100Hz.py &')

    time.sleep(5)

    update_sampcount()

    while(any(x in os.popen(ps_test).read() for x in scriptNames)) == True:

    ## Check for wifi

            if check_wifi(IgnoreWIFI) == "Connected":
                kill_sampling(scriptNames)
                flash()
                exit(0)

            else:
                print("Sampling")
                time.sleep(5)

    print('Goodbye')
#    GPIO.output(wifi, 0)
    time.sleep(5)
#    os.system('sudo shutdown now')
