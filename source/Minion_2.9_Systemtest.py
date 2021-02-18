#! /usr/bin/env python

# This is the Minion 2.9 test script

import RPi.GPIO as GPIO
import time
import os

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def yes_no(answer):
    yes = set(['yes','y', 'ye', 'yeet', ''])
    no = set(['no','n'])

    while True:
        choice = raw_input(answer).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'\n")


print("Welcome to the Minion 2.9 test script")
print("This script is informed by the config file, be sure to enable all connected hardware before continuing")

answer = yes_no("Do you wish to continue?")

if answer == False:
    exit(0)

import math
import configparser
import sys
import pickle

i = 0

light = 12
BURN = 33
data_rec = 16
data_ext = 32


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(BURN, GPIO.OUT)
GPIO.setup(data_rec, GPIO.OUT)
GPIO.setup(data_ext, GPIO.OUT)
GPIO.output(light, 0)
GPIO.output(BURN, 0)
GPIO.output(data_rec, 0)
GPIO.output(data_ext, 0)


answer = raw_input("Test Pi controlled lights [ENTER]")


j = 0
while j <= 2:
        GPIO.output(light, 1)
        GPIO.output(data_rec, 1)
        GPIO.output(data_ext, 1)
        time.sleep(.25)
        GPIO.output(light, 0)
        GPIO.output(data_rec, 0)
        GPIO.output(data_ext, 0)
        time.sleep(.25)
        j = j + 1


GPIO.output(BURN, 1)

answer = raw_input("Check Burn Wire Voltage and press [ENTER] to continue")

GPIO.output(BURN, 0)

print("Processing config file")

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
iniTpp = str2bool(config['Sampling_scripts']['TempPres'])
iniTmp = str2bool(config['Sampling_scripts']['Temperature'])
iniO2  = str2bool(config['Sampling_scripts']['Oxybase'])
iniAcc = str2bool(config['Sampling_scripts']['ACC_100Hz'])

print("Days : {}".format(Ddays))
print("Hours: {}".format(Dhours))
print("Sample rate (hours) - {}".format(Srate))
TotalSamples = (((Ddays*24)+Dhours))/Srate
print("Total Cycles ------- {}".format(TotalSamples))

print("------------------------")

print("Enabled Devices:")

if iniTpp == True:
    print("Temperature and Pressure Sensor")

if iniImg == True:
    print("Raspberry Pi Camera")

if iniO2 == True:
    print("Oxybase O2 Sensor")

if iniAcc == True:
    print("Accelerometer")

print("------------------------")

answer = yes_no("Do you wish to begin sensor testing?")

if answer == False:
    print("Moving on...")

if iniImg == True and answer == True:
    print("Testing RPi Camera, image saved to /home/pi/Desktop/")

    from picamera import PiCamera

    camera = PiCamera()

    try:
        # Collect time value from pickle on desktop
        firstp = open("/home/pi/Documents/Minion_scripts/timesamp.pkl","rb")
        samp_time = pickle.load(firstp)
        samp_count = str(len(os.listdir("{}/minion_pics/".format(configDir)))+1)
        samp_time = "{}-{}".format(samp_count, samp_time)
        GPIO.output(light, 1)
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
        time.sleep(10)
        camera.capture('{}/{}-TEST.jpg'.format(configDir, samp_time))
        time.sleep(5)
        camera.stop_preview()
        GPIO.output(light, 0)
        print("{}-TEST.jpg").format(samp_time)

    except:
        print("Camera error")
        camera.stop_preview()
        GPIO.output(light, 0)


if iniTpp == True and answer == True:
    print("Testing Pressure and temperature sensor, data saved to /home/pi/Desktop/")

    import tsys01
    import ms5837

    NumSamples = 0

    MAX_Depth = float(config['Mission']['Max_Depth'])
    MAX_Depth = MAX_Depth*100.4  # Convert from meters to mBar
    iniTpp = str2bool(config['Sampling_scripts']['TempPres'])
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
            samp_count = int(samp_count) + 1

    samp_time = "{}-{}".format(samp_count, samp_time)

    file_name = "{}/{}_TEMPPRES-TEST.txt".format(configDir, samp_time)

    sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

    if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)

    # We have to read values from sensor to update pressure and temperature
    if not sensor.read():
        print("Sensor read failed!")
        exit(1)

    print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
    sensor.pressure(ms5837.UNITS_atm),
    sensor.pressure(ms5837.UNITS_Torr),
    sensor.pressure(ms5837.UNITS_psi))

    print("Temperature: %.2f C") % (sensor.temperature(ms5837.UNITS_Centigrade))

    freshwaterDepth = sensor.depth() # default is freshwater
    sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
    saltwaterDepth = sensor.depth() # No nead to read() again
    sensor.setFluidDensity(1000) # kg/m^3
    print("Depth: %.3f m (saltwater)") % (saltwaterDepth)

    # fluidDensity doesn't matter for altitude() (always MSL air density)
    print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

    time.sleep(1)

    file = open(file_name,"a+")

    if iniTmp == True:

        sensor_temp = tsys01.TSYS01()

        # We must initialize the sensor before reading it
        if not sensor_temp.init():
            print("Error initializing sensor")
            exit(1)

        file.write("T+P MS5837_30BA and TempTSYS01 @ %s\r\n" % samp_time)
        file.write("Pressure(mbar), Temp(C), TempTSYS01(C) \r\n")

    else:

        file.write("T+P MS5837_30BA @ %s\r\n" % samp_time)
        file.write("Pressure(mbar),Temp(C) \r\n")

    file.close()

    while NumSamples <= 10:

        if sensor.read():
            print("P: %0.1f mbar  %0.3f atm\tT: %0.2f C") % (
            sensor.pressure(), # Default is mbar (no arguments)
            sensor.pressure(ms5837.UNITS_atm), # Request psi
            sensor.temperature()) # Default is degrees C (no arguments)

        else:
            print('Sensor ded')
            file.write('Sensor fail')
            exit(1)

        if sensor.pressure() >= MAX_Depth:
            file.write("Minion Exceeded Depth Maximum!")
            abortMission(configLoc)

        file = open(file_name,"a")

        if iniTmp == True:

            if not sensor_temp.read():
                print("Error reading sensor")
                file.write("Error reading TSYS01, disabling.")
                iniTmp = False

            print("Temperature_accurate: %0.2f C" % sensor_temp.temperature())

            file.write("{},{},{}\n".format(sensor.pressure(), sensor.temperature(),sensor_temp.temperature()))

        else:

            file.write("{},{}\n".format(sensor.pressure(), sensor.temperature()))

        NumSamples = NumSamples + 1

        time.sleep(Sf)

    file.close()


if iniO2 == True and answer == True:
    print("Testing Oxybase O2 sensor, data saved to /home/pi/Desktop/")

    import serial

    ser= serial.Serial(
        port='/dev/serial0', #serial port the object should read
        baudrate= 19200,      #rate at which information is transfered over comm channel
        parity=serial.PARITY_NONE, #no parity checking
        stopbits=serial.STOPBITS_ONE, #pattern of bits to expect which indicates the end of a character
        bytesize=serial.EIGHTBITS, #number of data bits
        timeout=1
    )

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

    file_name = "{}/{}_OXYBASE-TEST.txt".format(configDir, samp_time)

    file = open(file_name,"a+")

    file.write("{}\r\n".format(file_name))

    file.write("Oxygen @ %s\r\n" % samp_time)
    file.write("Sample Rate: %sHz \n" % Srate)

    while(i < 10):

        ser.write(b'data\r')

        reply = ser.read_until('\r')

        file.write(reply)

        print(reply)

        i = i + 1

        time.sleep(Sf)

    ser.write(b'mode0000\r')


if iniAcc == True and answer == True:
    print("Testing Accelerometer, data saved to /home/pi/Desktop/")

    import Adafruit_ADXL345

    #Configure ADXL345
    accel = Adafruit_ADXL345.ADXL345()
    accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_100_HZ)

    firstp = open("timesamp.pkl","rb")
    samp_time = pickle.load(firstp)

    for dataNum in os.listdir('{}/minion_data/'.format(configDir)):
        if dataNum.endswith('_ACC.txt'):
            samp_count = samp_count + 1

    samp_time = "{}-{}".format(samp_count, samp_time)

    file_name = "{}/{}_ACC-TEST.txt".format(configDir, samp_time)

    file = open(file_name,"a+")

    file.write("%s\r\n" % samp_time)
    file.write("X,Y,Z = +/- 2g\r\n")

    while NumSamples < 10:
        # Read the X, Y, Z axis acceleration values and print them.
        x, y, z = accel.read()
        file.write('{0},{1},{2}\n'.format(x, y, z))
        NumSamples = NumSamples + 1


answer = yes_no("Do you wish to continue to GPS testing?")

if answer == False:
    print("Done!")
    exit(0)

    print("Testing GPS for reception")

    import minsat
    from minsat import MinSat

    gps_port = "/dev/ttySC0"
    gps_baud = 9600
    modem_port = "/dev/ttySC1"
    modem_baud = 19200

    m1 = MinSat(gps_port,gps_baud,modem_port,modem_baud)

    def display_gps_resp_struct(ret_info):
        print("="*50)
        print("Valid Position: " + str(ret_info.valid_position))
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                ret_info.tm_mon,  # Grab parts of the time from the
                ret_info.tm_mday,  # struct_time object that holds
                ret_info.tm_year,  # the fix time.  Note you might
                ret_info.tm_hour,  # not get all data like year, day,
                ret_info.tm_min,  # month!
                ret_info.tm_sec,
            )
        )
        print("Latitude,Longitude: {:.6f},{:06f}".format(ret_info.latitude,ret_info.longitude))
        print("="*50)


    ret_data = m1.gps_get_position(verbose=True)
    display_gps_resp_struct(ret_data)

print("Done!")