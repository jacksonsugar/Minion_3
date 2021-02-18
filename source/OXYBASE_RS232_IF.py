import os
import time
import serial
import configparser
import pickle

samp_count = 1

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)

config = configparser.ConfigParser()
config.read(configLoc)

reply = ''

i = 1

ser= serial.Serial(
    port='/dev/serial0', #serial port the object should read
    baudrate= 19200,      #rate at which information is transfered over comm channel
    parity=serial.PARITY_NONE, #no parity checking
    stopbits=serial.STOPBITS_ONE, #pattern of bits to expect which indicates the end of a character
    bytesize=serial.EIGHTBITS, #number of data bits
    timeout=1
)

firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
samp_time = pickle.load(firstp)

if len(os.listdir('{}/minion_pics'.format(configDir))) == 0 and len(os.listdir('{}/minion_data/INI'.format(configDir))) == 0:

    Stime = float(config['Initial_Samples']['hours'])
    Srate = float(config['Initial_Samples']['Oxygen_sample_rate'])

    for dataNum in os.listdir('{}/minion_data/INI/'.format(configDir)):
        if dataNum.endswith('_OXY-INI.txt'):
            samp_count = samp_count + 1

    samp_time = "{}-{}".format(samp_count, samp_time)

    file_name = "{}/minion_data/INI/{}_OXY-INI.txt".format(configDir, samp_time)

else:

    Stime = float(config['Final_Samples']['hours'])
    Srate = float(config['Final_Samples']['Oxygen_sample_rate'])

    for dataNum in os.listdir('{}/minion_data/FIN/'.format(configDir)):
        if dataNum.endswith('_OXY-FIN.txt'):
            samp_count = samp_count + 1

    samp_time = "{}-{}".format(samp_count, samp_time)

    file_name = "{}/minion_data/FIN/{}_OXY-FIN.txt".format(configDir, samp_time)

Sample_number = (Stime*3600*Srate)
Sf = 1/Srate

time.sleep(1)

ser.flushInput()
ser.flushOutput()

ser.write(b'mode0001\r')

file = open(file_name,"a+")

file.write("{}\r\n".format(file_name))

file.write("OXYBASE RS232 Dissolved Oxygen @ %s\r\n" % samp_time)
file.write("Sample Rate: %sHz \n" % Sf)

while(Sample_number > i):

    ser.write(b'data\r')

    reply = ser.read_until('\r')

    file.write(reply)

    print(reply)

    i = i + 1

    time.sleep(Sf)

ser.write(b'mode0000\r')
