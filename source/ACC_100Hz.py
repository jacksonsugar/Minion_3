 #!/usr/bin/env python

# Quick data recording script for the ADXL345

import os
from adxl345 import ADXL345
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

TotalSamples = Stime*60*100*4

#Configure ADXL345
accel = ADXL345()

firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
samp_time = pickle.load(firstp)

for dataNum in os.listdir('{}/minion_data/'.format(configDir)):
    if dataNum.endswith('_ACC.txt'):
        samp_count = samp_count + 1

samp_time = "{}-{}".format(samp_count, samp_time)

file_name = "/home/pi/Desktop/minion_data/%s_ACC.txt" % samp_time

file = open(file_name,"a+")

file.write("%s\r\n" % samp_time)
file.write("X,Y,Z = +/- 2g\r\n")

while NumSamples <= TotalSamples:

    tic = time.perf_counter()

    try:
        # Read the X, Y, Z axis acceleration values and print them.
        axes = accel.getAxes(True)
        print('{},{},{}'.format(axes['x'],axes['y'],axes['z']))
        file.write('{},{},{}\n'.format(axes['x'], axes['y'], axes['z']))

        NumSamples = NumSamples + 1

        toc = time.perf_counter()

        timeS = toc - tic

        if timeS >= .05:
            timeS = .05

        time.sleep(.05 - timeS)

    except:
        print('acc broken')
