import serial
from ctypes import *
import time

gpio = CDLL('./SC16IS752GPIO.so')
OUT = 1
IN = 0

gpio.SC16IS752GPIO_Init()
time.sleep(1) #give the pi about 1 second to export the pins

gpio.SC16IS752GPIO_Mode(7,OUT) #GPS PWR PIN
gpio.SC16IS752GPIO_Mode(3,OUT) #9602 PWR PIN

gpio.SC16IS752GPIO_Write(7,1)  #GPS PWR ON

ser = serial.Serial('/dev/ttySC0',9600,timeout=10)

try:
    while True:
        x = ser.read()
        print(x)
except KeyboardInterrupt:
    gpio.SC16IS752GPIO_Write(7,0)  #GPS PWR OFF
    pass
