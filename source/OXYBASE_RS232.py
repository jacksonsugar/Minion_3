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

Stime = config['Data_Sample']['Minion_sample_time']

try :
    float(test_string)
    Stime = float(Stime)
except :
    Stime = float(.2)

Srate = float(config['Data_Sample']['Oxygen_sample_rate'])

Sample_number = Stime*60*Srate
Sf = 1/Srate

time.sleep(1)

ser.flushInput()
ser.flushOutput()

ser.write(b'mode0001\r')

firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
samp_time = pickle.load(firstp)

for dataNum in os.listdir('{}/minion_data/'.format(configDir)):
    if dataNum.endswith('_OXYBASE.txt'):
        samp_count = samp_count + 1

samp_time = "{}-{}".format(samp_count, samp_time)

file_name = "{}/minion_data/{}_OXYBASE.txt".format(configDir, samp_time)

file = open(file_name,"a+")

file.write("{}\r\n".format(file_name))

file.write("Oxygen @ %s\r\n" % samp_time)
file.write("Sample Rate: %sHz \n" % Srate)

while(Sample_number > i):

    ser.write(b'data\r')

    reply = ser.read_until('\r')

    file.write(reply)

    print(reply)

    i = i + 1

    time.sleep(Sf)

ser.write(b'mode0000\r')