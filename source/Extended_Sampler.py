#!/usr/bin/env python3
import RPi.GPIO as GPIO
import tsys01
import ms5837
from kellerLD import KellerLD
import pickle
import time
import os
import math
import configparser
import sys

BURN = 33
data_rec = 16

samp_count = 1

NumSamples = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BURN, GPIO.OUT)
GPIO.setup(data_rec, GPIO.OUT)
GPIO.output(BURN, 0)
GPIO.output(data_rec, 1)

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def abortMission(configLoc):

    abortConfig = configparser.ConfigParser()
    abortConfig.read(configLoc)
    abortConfig.set('Mission','Abort','1')
    with open(config,'wb') as abortFile:
        abortConfig.write(abortFile)

    GPIO.output(IO328, 0)
    os.system('sudo python /home/pi/Documents/Minion_scripts/Recovery_Sampler.py &')

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)
config = configparser.ConfigParser()
config.read(configLoc)
MAX_Depth = float(config['Mission']['Max_Depth'])
MAX_Depth = MAX_Depth*100.4  # Convert from meters to mBar
Abort = str2bool(config['Mission']['Abort'])
iniImg = str2bool(config['Sampling_scripts']['Image'])
iniP30 = str2bool(config['Sampling_scripts']['30Ba-Pres'])
iniP100 = str2bool(config['Sampling_scripts']['100Ba-Pres'])
iniTmp = str2bool(config['Sampling_scripts']['Temperature'])
iniO2  = str2bool(config['Sampling_scripts']['Oxybase'])
iniAcc = str2bool(config['Sampling_scripts']['ACC_100Hz'])

if Abort == True:
        GPIO.output(IO328, 0)
        os.system('sudo python /home/pi/Documents/Minion_scripts/Recovery_Sampler.py &')


firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
samp_time = pickle.load(firstp)

for dataNum in os.listdir('{}/minion_data/INI/'.format(configDir)):
    if dataNum.endswith('_TEMPPRES-INI.txt'):
        samp_count = samp_count + 1

samp_time = "{}-{}".format(samp_count, samp_time)

Stime = float(config['Initial_Samples']['hours'])
Srate = float(config['Initial_Samples']['TempPres_sample_rate'])    

file_name = "{}/minion_data/INI/{}_TEMPPRES-INI.txt".format(configDir, samp_time)

Sf = 1/Srate

TotalSamples = Stime*60*60*Srate

######################

time.sleep(1)

file = open(file_name,"a+")

file.write("{}_TEMPPRES.txt".format(samp_time))

if iniP30 == True:

    Psensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

    if not Psensor.init():
        print("Failed to initialize P30 sensor!")
        exit(1)

    # We have to read values from sensor to update pressure and temperature
    if Psensor.read():
        Pres_ini = Psensor.pressure()
    else:
        Pres_ini = "Broken"

    file.write("Pressure(mbar),Temp(C)")

if iniP100 == True:

    Psensor = KellerLD()

    if not Psensor.init():
        print("Failed to initialize P100 sensor!")
        exit(1)
    # We have to read values from sensor to update pressure and temperature
    if Psensor.read():
        Pres_ini = Psensor.pressure()
    else:
        Pres_ini = "Broken"

    file.write("Pressure(mbar),Temp(C)")

if iniTmp == True:

    sensor_temp = tsys01.TSYS01()

    # We must initialize the sensor before reading it
    if not sensor_temp.init():
        print("Error initializing Temperature sensor")
        exit(1)

    file.write(", TempTSYS01(C)")

file.write("\r\n")
file.close()


if __name__ == '__main__':


    if iniImg == True:
        os.system('sudo python /home/pi/Documents/Minion_scripts/Minion_image_IF.py &')

    if iniO2 == True:
        os.system('sudo python /home/pi/Documents/Minion_scripts/OXYBASE_RS232_IF.py &')

    if iniAcc == True:
        os.system('sudo python /home/pi/Documents/Minion_scripts/ACC_100Hz_IF.py &')

    # Spew readings
    while NumSamples <= TotalSamples:

        file = open(file_name,"a")

        sensor_string = ''

        if iniP100 or iniP30 == True:

            if Psensor.read():
                Ppressure = Psensor.pressure()
                Ptemperature = Psensor.temperature()
                Pres_data = "{},{},".format(Ppressure, Ptemperature)
                print("Pressure sensor data: {}".format(Pres_data))
                sensor_string = "{}{}".format(sensor_string,Pres_data)

            else:
                print('Pressure Sensor ded')
                file.write('Pressure Sensor fail')
                abortMission(configLoc)
            
            if Ppressure >= MAX_Depth:
                file.write("Minion Exceeded Depth Maximum!")
                abortMission(configLoc)


        if iniTmp == True:

            if not sensor_temp.read():
                print("Error reading sensor")
                iniTmp = False

            Temp_acc = sensor_temp.temperature()

            print("Temperature_accurate: {} C".format(Temp_acc))

            sensor_string = '{}{}'.format(sensor_string, Temp_acc)

        
        file.write("{}\n".format(sensor_string))

        NumSamples = NumSamples + 1

        time.sleep(Sf)

    file.close()
    GPIO.output(data_rec, 0)
