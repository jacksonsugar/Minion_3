 #!/usr/bin/env python

# Quick data recording script for the ADXL345

import os
import Adafruit_ADXL345
import configparser
import pickle

samp_count = 1

NumSamples = 0

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']

config = configparser.ConfigParser()
configloc = '{}/Minion_config.ini'.format(configDir)

config.read(configloc)

Stime = config['Data_Sample']['Minion_sample_time']

try :
    float(test_string)
    Stime = float(Stime)
except :
    Stime = float(.2)

TotalSamples = Stime*60*100

#Configure ADXL345
accel = Adafruit_ADXL345.ADXL345()
accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_100_HZ)

firstp = open("timesamp.pkl","rb")
samp_time = pickle.load(firstp)

for dataNum in os.listdir('{}/minion_data/'.format(configDir)):
    if dataNum.endswith('_ACC.txt'):
        samp_count = samp_count + 1

samp_time = "{}-{}".format(samp_count, samp_time)

file_name = "/home/pi/Documents/minion_data/%s_ACC.txt" % samp_time

file = open(file_name,"a+")

file.write("%s\r\n" % samp_time)
file.write("X,Y,Z = +/- 2g\r\n")

while NumSamples <= TotalSamples:
    # Read the X, Y, Z axis acceleration values and print them.
    x, y, z = accel.read()
    file.write('{0},{1},{2}\n'.format(x, y, z))
    NumSamples = NumSamples + 1

