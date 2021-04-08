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

config = configparser.ConfigParser()
configLoc = '{}/Minion_config.ini'.format(configDir)

config.read(configLoc)
MAX_Depth = float(config['Mission']['Max_Depth'])
MAX_Depth = MAX_Depth*100.4  # Convert from meters to mBar
iniP30 = str2bool(config['Sampling_scripts']['30Ba-Pres'])
iniP100 = str2bool(config['Sampling_scripts']['100Ba-Pres'])
iniTmp = str2bool(config['Sampling_scripts']['Temperature'])

Stime = config['Data_Sample']['Minion_sample_time']

try :
    float(test_string)
    Stime = float(Stime)
except :
    Stime = float(.2)

Srate = float(config['Data_Sample']['Minion_sample_rate'])

Sf = 1/Srate

TotalSamples = Stime*60*Srate

firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
samp_time = pickle.load(firstp)

for dataNum in os.listdir('{}/minion_data/'.format(configDir)):
    if dataNum.endswith('_TEMPPRES.txt'):
        samp_count = samp_count + 1

samp_time = "{}-{}".format(samp_count, samp_time)

file_name = "{}/minion_data/{}_TEMPPRES.txt".format(configDir, samp_time)

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


