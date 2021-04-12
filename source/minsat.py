from ctypes import CDLL
import time
import serial
import sys
import os
import math
import random
import configparser
#Load the shared object file for GPIO Drivers
gpio =  CDLL('/home/pi/Documents/Minion_scripts/SC16IS752GPIO.so')

DEV_ID = str('01')

data_config = configparser.ConfigParser()
data_config.read('/home/pi/Documents/Minion_scripts/Data_config.ini')

configDir = data_config['Data_Dir']['Directory']
configLoc = '{}/Minion_config.ini'.format(configDir)
config = configparser.ConfigParser()
config.read(configLoc)

MINION_ID = str(config['MINION']['Number']).zfill(3)

#Definitions
OUT = 1
IN = 0
SET = 1
RESET = 0
#ON=1
#OFF=0

#Pin Assignments:
LOAD_SW_ENA = 0
REG_5V_ENA = 1
UNUSED_PIN_2 = 2
MODEM_ON_OFF = 3
NW_AVL = 4
UNUSED_PIN_5 = 5
UNUSED_PIN_6 = 6
GPS_PWR_ENA = 7

class MinSat():
    dev_on = 0x0A
    dev_off = 0x0B
    gps_com_port = ''
    modem_com_port = ''
    gps_baud = 9600
    modem_baud = 19200

    def __init__(self,gps_com_port,gps_baud,modem_com_port,modem_baud):
        """Iridium Short Burst Data and GPS Support for the Minion.

        Parameters
        ----------
        gps_com_port : 'string' Com Port Assigned to the GPS Module
        gps_baud : GPS baud rate
        modem_com_port : 'string' Com Port Assigned to the Iridiim Modem
        modem_baud: Iridium Modem baud rate
        """
        self.gps_com_port = gps_com_port
        self.gps_baud = gps_baud
        self.modem_com_port = modem_com_port
        self.modem_baud = modem_baud

        print("Initializing MinSat...")
        self.init_gpio_bank()
        print("MinSat Initialization Complete.")
#       pass

    def init_gpio(self):
        """Exports the pin definitions on the RPi."""

        gpio.SC16IS752GPIO_Init()

    def init_gpio_bank(self):
        """Exports the pin definitions on the RPi, sets the default pin directions and states."""

        print("Exporting Pins..."),
        gpio.SC16IS752GPIO_Init()
        #A delay is important - 1 seconds works - the RPi needs time to export the pins!
        time.sleep(1)
        print("Okay")
        #configure the pin direction
        print("Configuring Pin Direction..."),
        gpio.SC16IS752GPIO_Mode(LOAD_SW_ENA,OUT)
        gpio.SC16IS752GPIO_Mode(REG_5V_ENA,OUT)
        gpio.SC16IS752GPIO_Mode(MODEM_ON_OFF,OUT)
        gpio.SC16IS752GPIO_Mode(NW_AVL,IN)
        gpio.SC16IS752GPIO_Mode(GPS_PWR_ENA,OUT)
        gpio.SC16IS752GPIO_Mode(UNUSED_PIN_2,IN)
        gpio.SC16IS752GPIO_Mode(UNUSED_PIN_5,IN)
        gpio.SC16IS752GPIO_Mode(UNUSED_PIN_6,IN)
        print("Okay")
        #configure the output pin default states
        print("Configuring Output Pin Default States..."),
        gpio.SC16IS752GPIO_Write(LOAD_SW_ENA,RESET)
        gpio.SC16IS752GPIO_Write(REG_5V_ENA,RESET)
        gpio.SC16IS752GPIO_Write(MODEM_ON_OFF,RESET)
        gpio.SC16IS752GPIO_Write(GPS_PWR_ENA,RESET)
        print("Okay")

    def modem_pwr(self,state):
        """Turn the Iridium 9602 Modem on or off.

        Parameters
        ----------
        state : dev_on or dev_off

        """
        if state == self.dev_on:
            gpio.SC16IS752GPIO_Write(LOAD_SW_ENA,SET)
            time.sleep(.25)
            gpio.SC16IS752GPIO_Write(REG_5V_ENA,SET)
            time.sleep(.25)
            gpio.SC16IS752GPIO_Write(MODEM_ON_OFF,SET)
        elif state == self.dev_off:
            gpio.SC16IS752GPIO_Write(MODEM_ON_OFF,RESET)
            time.sleep(.1)
            gpio.SC16IS752GPIO_Write(REG_5V_ENA,RESET)
            time.sleep(.1)
            gpio.SC16IS752GPIO_Write(LOAD_SW_ENA,RESET)
        else:
            print('Out of Range')

    class GPSStruct:
        def __init__(self):
            """GPS Time and Position Data

            Members
            -------
            valid_position:   True or False
            latitude:         Latitude
            longitude:        Longitude
            tm_mon:           Month
            tm_mday:          Day
            tm_year:          Year
            tm_hour:          Hour
            tm_min:           Minute
            tm_sec:           Seconds

            """
            self.valid_position = False
            self.tm_mon = 0
            self.tm_mday = 0
            self.tm_year = 0
            self.tm_hour = 0
            self.tm_min = 0
            self.tm_sec = 0
            self.latitude = 0
            self.longitude = 0

    def gps_pwr(self,state):
        """Turn the GPS Module on or off.

        Parameters
        ----------
        state : dev_on or dev_off

        """
        if state == self.dev_on:
            gpio.SC16IS752GPIO_Write(GPS_PWR_ENA,SET)
        elif state == self.dev_off:
            gpio.SC16IS752GPIO_Write(GPS_PWR_ENA,RESET)
        else:
            print('Out of Range')

    def _gps_stream(self):
        self.gps_pwr(self.dev_on)
        print("GPS Power On.")
        #uart = serial.Serial("/dev/ttySC0", baudrate=9600, timeout=10)
        uart = serial.Serial(self.gps_com_port, baudrate=self.gps_baud, timeout=10)
        gps = GPS(uart, debug=False)  # Use UART/pyserial
        last_print = time.time()
        try:
            while True:
                sentence = gps.readline()
                if not sentence:
                    continue
                print(str(sentence).strip())
        except KeyboardInterrupt:
            self.gps_pwr(self.dev_off)
            print("GPS Power Off.")
            pass            

    def gps_get_position(self,**kwargs):
        """Request a position from the GPS Module. 
        For increased accuracy, the fifth valid position is reported.
        Powers the GPS automatically and can maintain the power based on optional user input.

        Keyword Args:
        -------------
        gps_timeout : Timeout when acquiring a GPS position (default 120 seconds)
        maintain_gps_pwr : Keep the power on after position acquisition attempt (default False)
        first_fix : Report the first valid fix - may be less accurate (default False)
        verbose : displays additional information (default False)

        Returns:
        --------
        class GPSStruct : GPS Time and Position Data

        """

        #create a dictionary of default values
        options = {
            'gps_timeout' : 120,
            'maintain_gps_pwr' : False,
            'first_fix' : False,
            'verbose' : False,}

        options.update(kwargs) #Now update the dictionary with any duplicate keys from kwargs

        self.gps_pwr(self.dev_on)
        print("GPS Power On.")
        #uart = serial.Serial("/dev/ttySC0", baudrate=9600, timeout=10)
        uart = serial.Serial(self.gps_com_port, baudrate=self.gps_baud, timeout=10)
        gps = GPS(uart, debug=False)  # Use UART/pyserial
        gpsStruct = self. GPSStruct() #Create an instance of the GPSStruct()
        last_print = time.time()
        time_start = time.time()
        gpsTimeout = options['gps_timeout']
        if options['verbose'] == True:
            print("GPS Fix Timeout: " + str(gpsTimeout) + " seconds.")
        valid_position = False
        num_valid_fix = 0
        sys.stdout.write("Waiting for fix")
        sys.stdout.flush()
        while( valid_position == False and time.time() < time_start + gpsTimeout):
            gps.update()
            current = time.time()
            if current - last_print >= 1.0:
                last_print = current
                if not gps.has_fix:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    continue
                if not options['first_fix']:
                    if gps.has_fix:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                        num_valid_fix += 1
                        #print("Valid Fixes: " + str(num_valid_fix))
                        if num_valid_fix <5:
                            continue

                print("GPS Position Acquired.")
                valid_position = True

                #Now that we have a valid position, update the GPS Struct
                gpsStruct.valid_position = True
                gpsStruct.latitude = gps.latitude
                gpsStruct.longitude = gps.longitude
                gpsStruct.tm_mon = gps.timestamp_utc.tm_mon
                gpsStruct.tm_mday = gps.timestamp_utc.tm_mday
                gpsStruct.tm_year = gps.timestamp_utc.tm_year
                gpsStruct.tm_hour = gps.timestamp_utc.tm_hour
                gpsStruct.tm_min = gps.timestamp_utc.tm_min
                gpsStruct.tm_sec = gps.timestamp_utc.tm_sec

                if options['verbose'] == True:
                    #Display the data
                    print("=" * 40)  # Print a separator line.
                    print(
                        "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                            gps.timestamp_utc.tm_mday,  # struct_time object that holds
                            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                            gps.timestamp_utc.tm_min,  # month!
                            gps.timestamp_utc.tm_sec,
                            )
                    )
                    #print("Latitude: {0:.6f} degrees".format(gps.latitude))
                    #print("Longitude: {0:.6f} degrees".format(gps.longitude))
                    print("Latitude,Longitude: {:.6f},{:.6f}".format(gpsStruct.latitude,gpsStruct.longitude,))
                    #gpsStruct.latitude = gps.latitude
                    #gpsStruct.longitude = gps.longitude
                    print("=" * 40)

        if(valid_position == False):
            print("No GPS Position Available.")
        if options['maintain_gps_pwr'] == False:
            self.gps_pwr(self.dev_off)
            print("GPS Power Off.")
        else:
            print("GPS Power Maintained.")
        return gpsStruct
        pass

#   class rockBlockProtocol():
    def rockBlockConnected(self):pass
    def rockBlockDisconnected(self):pass
#   SIGNAL
    def rockBlockSignalUpdate(self,signal):pass
    def rockBlockSignalPass(self):pass
    def rockBlockSignalFail(self):pass
#   MT
    def rockBlockRxStarted(self):pass
    def rockBlockRxFailed(self):pass
    def rockBlockRxReceived(self,mtmsn,data):pass
    def rockBlockRxMessageQueue(self,count):pass
#   MO
#   def rockBlockTxStarted(self):pass
#   def rockBlockTxFailed(self):pass
#   def rockBlockTxSuccess(self,momsn):pass

    def rockBlockTxStarted(self):
        print("Iridium SBD Tx Started")

    def rockBlockTxFailed(self):
        print("Iridium SBD Tx Failed")

    def rockBlockTxSuccess(self,momsn):
        print("Iridium SBD Tx Success. MOMSN: " + str(momsn))

    class SBDFileSendResponseStruct:
        def __init__(self):
            """SBD File Transmission  Session Data

            Members:
            -------
            file_name:              File Name
            file_open_success:      True or Fale
            file_size:              Size of file in bytes
            xmt_file_complete:      True or False
            xmt_num_bytes:          Number of bytes transmitted
            xmt_num_sbd_success:    Number of Successful SBD Sessions
            xmt_num_sbd_required:   Number of SBD Sessions Required
            curr_file_loc:          Current Location in the File
            start_file_loc:         File Location Starting Point

            """
            self.file_name = ''
            self.file_open_success = False
            self.file_size = 0
            self.xmt_file_complete = False
            self.xmt_num_bytes = 0
            self.xmt_num_sbd_success = 0  #number of sbd sessions successfully transmitted
            self.xmt_num_sbd_req = 0 #number of sbd sessions required
            self.curr_file_loc = 0
            self.start_file_loc = 0

    def sbd_send_message(self,msg,**kwargs):
        """Send a 340 byte limited message via the Iridium Modem.
        Powers the modem automatically and can maintain the power based on optional user input.

        Parameters:
        -----------
        msg : Message to be sent

        Keyword arguments:
        ------------------
        ird_sig_timeout : Timeout in seconds waiting for Iridium satellite signal (default 120 seconds)
        maintain_ird_pwr : Keep the Iridium modem powered after a transmission attempt (default False)
        verbose : Displays additional information (default False)

        Returns:
        --------
        bool : True if message sent successfully, False otherwise

        """

        options = {
           'ird_sig_timeout' : 120,
           'maintain_ird_pwr' : False,
           'verbose' : False,}
        options.update(kwargs) #update the dictionary with any duplicate values

        if len(msg) > 340:
            print("Data is greater than 340 byte limit.")
            return False
        self.modem_pwr(self.dev_on)
        print("Iridium Power On.")
#       rockBlockProtocol()
        #rb=rockBlock("/dev/ttySC1",self)
        rb=rockBlock(self.modem_com_port,self.modem_baud,self)
        if options['verbose'] == True:
            modemSN = rb.getSerialIdentifier()
            print("Iridium Modem IMEI: " + str(modemSN))

        sigStrength = 0
        sigDetectFlag = 0
        iridiumSignalTimeout =  options['ird_sig_timeout'] #timeout in seconds
        if options['verbose'] == True:
            print("Iridium Signal Timeout: " + str(iridiumSignalTimeout) + " seconds")
        sys.stdout.write("Waiting for Iridium Signal")
        sys.stdout.flush()
        time_start = time.time()
        while(time.time() < time_start + iridiumSignalTimeout):
            sys.stdout.write(".")
            sys.stdout.flush()
            sigStrength = rb.requestSignalStrength()
            time.sleep(.1)
            if sigStrength > 0:
                sigDetectFlag = 1
                break

        if(sigDetectFlag == 0):
            print("No Signal.")
            rb.close()
            if options['maintain_ird_pwr'] == False:
                self.modem_pwr(self.dev_off)
                print("Iridium Power Off.")
            return False
        else:
            print("Signal Detected.")

        if options['verbose'] == True:
            print("Sending Message: " + msg)
        msg_success = rb.sendMessage(msg)
        #print("Sleeping for Test")
        #time.sleep(5)
        rb.close()
        if options['maintain_ird_pwr'] == False:
            self.modem_pwr(self.dev_off)
            print("Iridium Power Off.")
        else:
            print("Iridium Power Maintained.")
        return msg_success


    def sbd_send_file(self,fname,**kwargs):
        """Send a file via the Iridium Modem.

        Parameters:
        -----------
        fname : File Name

        Keyword Arguments:
        ------------------
        num_header_lines : Number of header lines to include with each SBD Message (default 0)
        start_file_position : Position in file from which to start sending SBD messages (default 0)
        ird_sig_timeout : Timeout in seconds waiting for Iridium satellite signal (default 120 seconds)
        verbose : Display additional information (default False)

        Returns:
        --------
        class SBDFileSendResponseStruct

        """

        max_sbd_size = 340

        #Create an instance of SBDFileSendStruct
        sbdFileSendResponseStruct = self.SBDFileSendResponseStruct()

        #Update the file name in the return struct
        sbdFileSendResponseStruct.file_name = fname

        #Create a dictionary of default values
        options = {
            'num_header_lines' : 0,
            'start_file_position' : 0,
            'ird_sig_timeout' : 120,
            'verbose' : False,}

        options.update(kwargs) #Now update that dictionary with any duplicate keys from kwargs

        num_header_lines = options["num_header_lines"]
        start_file_position = options["start_file_position"]
        sbdFileSendResponseStruct.start_file_loc = start_file_position #Update the return struct

        #Try to open the file. If we cannot open the file, update the return struct and exit
        try:
            f_object = open(fname, 'rb')
            file_stats = os.stat(fname)
            file_size =  file_stats.st_size
            sbdFileSendResponseStruct.file_size = file_size
            sbdFileSendResponseStruct.file_open_success = True
        except:
            print("!!! Could not open file: " + fname + " !!!")
            sbdFileSendResponseStruct.file_open_success = False
            return sbdFileSendResponseStruct

        #Read in the header lines:
        header = bytearray()  #initialize header to empty
        for idx in range(num_header_lines):
            header += f_object.readline()

        #Navigate to where we left off
        if start_file_position > 0:
            f_object.seek(start_file_position)

        num_sbd_required = int(math.ceil((float(file_stats.st_size)-start_file_position)/(max_sbd_size-len(header))))
        sbdFileSendResponseStruct.xmt_num_sbd_req = num_sbd_required #update the response struct

        if options['verbose'] == True:
            print("-" * 60)
            print("File Size: " + str(file_stats.st_size) + " bytes")
            print("Starting Transmissions at File Location: " + str(start_file_position))
            print("Number of SBD Sessions Required: " + str(num_sbd_required))
            print("Header: " + header.decode('ascii'))
            print("-" * 60)

        #num_successful_sbd_to_send = random.randint(0,9) #this is for testing purposes only!!!

        num_sbd_sent = 0

        #Main Sending Loop
        for x in range(int(num_sbd_required)):
            fileLoc = f_object.tell()
            data = header + f_object.read(max_sbd_size-len(header))
            print("-" * 50)
            print("Block #" + str(x+1) + "    Length: " + str(len(data)) + " bytes" + "    File Location: " + str(fileLoc))
            if options['verbose'] == True:
                print(data.decode('ascii'))
            resp =  self.sbd_send_message(data.decode('ascii'),maintain_ird_pwr=True,verbose=False,ird_sig_timeout=options['ird_sig_timeout'])
            if resp == False:
            #if x  == num_successful_sbd_to_send:  #this is for testing purposes only!!!
                print("SBD Transmit Failed.")
                print(" ")
                sbdFileSendResponseStruct.xmt_file_complete = False
                sbdFileSendResponseStruct.curr_file_loc = fileLoc
                sbdFileSendResponseStruct.xmt_num_sbd_success = num_sbd_sent
                self.modem_pwr(self.dev_off)    #shut down the modem
                print("Iridium Modem Powered Down.")
                f_object.close()    #close the file
                return sbdFileSendResponseStruct
            print("SBD Transmit Success")
            print(" ")
            num_sbd_sent += 1
            sbdFileSendResponseStruct.xmt_num_bytes += len(data)

        #Update the response struct
        sbdFileSendResponseStruct.xmt_file_complete = True
        sbdFileSendResponseStruct.curr_file_loc = f_object.tell() #if the entire file was transmitted this should be the last byte
        sbdFileSendResponseStruct.xmt_num_sbd_success = num_sbd_sent

        self.modem_pwr(self.dev_off)    #shut down the modem
        print("Iridium Modem Powered Down.")
        f_object.close()    #close the file

        return sbdFileSendResponseStruct

    def sbd_send_position(self,**kwargs):
        """Acquire and Transmit a GPS Position via the Iridium Modem.
        Powers the GPS automatically and can maintain the power based on optional user input.

        Keyword Arguments:
        -------------
        gps_timeout : Timeout when acquiring a GPS position (default 120 seconds)
        ird_sig_timeout : Timeout in seconds waiting for Iridium satellite signal (default 120 seconds)
        maintain_gps_pwr : Keep the GPS power on after position acquisition attempt (default False)
        maintain_ird_pwr : Keep the Iridium modem powered after a transmission attempt (default False)
        verbose : displays additional information (default False)

        Returns:
        --------
        bool : True if acquired and sent successfully, False otherwise
        class GPSStruct : GPS Time and Position Data

        """

        #create a dictionary of default values
        options = {
            'gps_timeout' : 120,
            'ird_sig_timeout' : 120,
            'maintain_gps_pwr' : False,
            'maintain_ird_pwr' : False,
            'verbose' : False,}

        options.update(kwargs) #Now update the dictionary with any duplicate keys from kwargs

        gpsData = self.gps_get_position(verbose=options['verbose'],gps_timeout=options['gps_timeout'],ird_sig_timeout=options['ird_sig_timeout'],maintain_gps_pwr=options['maintain_gps_pwr'],maintain_ird_pwr=options['maintain_ird_pwr'])

        gpsDataStr = "{},{},{:04},{:02},{:02},{:02},{:02},{:02},{:.6f},{:.6f}".format(
            DEV_ID,
            MINION_ID,
            gpsData.tm_year,
            gpsData.tm_mon,
            gpsData.tm_mday,
            gpsData.tm_hour,
            gpsData.tm_min,
            gpsData.tm_sec,
            gpsData.latitude,
            gpsData.longitude,
            )
        print("SBD msg = ".format(gpsDataStr))
        if gpsData. valid_position == True:
            if options['verbose'] == True:
                print("GPS Position Acquired.")
                print("GPS Data: " + gpsDataStr)
            if self.sbd_send_message(gpsDataStr) == True:
                return True, gpsData
            else:
                return False, gpsData
        else:
            if options['verbose'] == True:
                print("No Valid GPS Position.")
            return False, gpsData

################################################################################
################################################################################




################################################################################
################################################################################
#    Copyright 2015 Makersnake
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
   
import glob
import signal
import sys
import time

import serial

#class rockBlockProtocol(object):
    
#    def rockBlockConnected(self):pass
#    def rockBlockDisconnected(self):pass
    
    #SIGNAL
#    def rockBlockSignalUpdate(self,signal):pass
#    def rockBlockSignalPass(self):pass
#    def rockBlockSignalFail(self):pass
    
    #MT
#    def rockBlockRxStarted(self):pass
#    def rockBlockRxFailed(self):pass
#    def rockBlockRxReceived(self,mtmsn,data):pass
#    def rockBlockRxMessageQueue(self,count):pass
     
    #MO
#    def rockBlockTxStarted(self):pass
#    def rockBlockTxFailed(self):pass
#    def rockBlockTxSuccess(self,momsn):pass
    
class rockBlockException(Exception):
    pass
    
class rockBlock(object):
    
    IRIDIUM_EPOCH = 1399818235000   #May 11, 2014, at 14:23:55 (This will be 're-epoched' every couple of years!)
        
    def __init__(self, portId, portBaud, callback):
        
        self.s = None
        self.portId = portId
        self.portBaud = portBaud
        self.callback = callback
        self.autoSession = True     #When True, we'll automatically initiate additional sessions if more messages to download
        
        try:
            
            #self.s = serial.Serial(self.portId, 19200, timeout=5)
            self.s = serial.Serial(self.portId, self.portBaud, timeout=5)
            
            if( self._configurePort() ):
                print('Configured Iridium Port')                
                self.ping() #KEEP SACRIFICIAL!
                                            
                self.s.timeout = 60
                    
                if( self.ping() ):
                    
                    if(self.callback != None and callable(self.callback.rockBlockConnected) ):   
                        self.callback.rockBlockConnected()
                        
                        return
                                     
            
            self.close()
            raise rockBlockException()
                    
        except (Exception):
            
            raise rockBlockException
        
    
    #Ensure that the connection is still alive         
    def ping(self):
        print("***ping***")
        self._ensureConnectionStatus()
                
        command = "AT"
                
        self.s.write(command + "\r")
        
        if( self.s.readline().strip() == command ):
            
            if( self.s.readline().strip() == "OK" ):
                                                         
                return True
                                            
        return False
    
    #Handy function to check the connection is still alive, else throw an Exception
    def pingception(self):
        self._ensureConnectionStatus()
                
        self.s.timeout = 5
        if(self.ping() == False):
            
            raise rockBlockException
        
        self.s.timeout = 60
            
    def requestSignalStrength(self):
        self._ensureConnectionStatus()

        command = "AT+CSQ"
        
        self.s.write(command + "\r")
             
        if( self.s.readline().strip() == command):
        
            response = self.s.readline().strip()
                  
            if( response.find("+CSQ") >= 0 ):
                            
                self.s.readline().strip()    #OK
                self.s.readline().strip()    #BLANK
                                        
                if( len(response) == 6):
                
                    return int( response[5] )
            
        return -1   
     
    
    def messageCheck(self):
        self._ensureConnectionStatus()
        
        if(self.callback != None and callable(self.callback.rockBlockRxStarted) ):
            self.callback.rockBlockRxStarted()
                            
        if( self._attemptConnection() and self._attemptSession() ):
            
            return True
        
        else:
       
            if(self.callback != None and callable(self.callback.rockBlockRxFailed) ):
                self.callback.rockBlockRxFailed()
                
        
    def networkTime(self):
        self._ensureConnectionStatus()
         
        command = "AT-MSSTM"
                
        self.s.write(command + "\r")
        
        if(self.s.readline().strip() == command):
                
            response = self.s.readline().strip()
            
            self.s.readline().strip()   #BLANK
            self.s.readline().strip()   #OK
            
            if( not "no network service" in response ):
                
                utc = int(response[8:], 16)
                    
                utc = int((self.IRIDIUM_EPOCH + (utc * 90))/1000)
                
                return utc
          
            else:
                
                return 0;
                      
                            
    def sendMessage(self, msg):
        self._ensureConnectionStatus()
                
        if(self.callback != None and callable(self.callback.rockBlockTxStarted) ):
            self.callback.rockBlockTxStarted()
        
        if( self._queueMessage(msg) and self._attemptConnection()  ):
        
            SESSION_DELAY = 1
            SESSION_ATTEMPTS = 3
            
            while(True):
                    
                SESSION_ATTEMPTS = SESSION_ATTEMPTS - 1
                
                if(SESSION_ATTEMPTS == 0):
                                        
                    break
                
                if( self._attemptSession() ):
                    
                    return True
                
                else:
                    
                    time.sleep(SESSION_DELAY)
                            
        if(self.callback != None and callable(self.callback.rockBlockTxFailed) ):
            self.callback.rockBlockTxFailed()
            
        return False
    
    
    def getSerialIdentifier(self):
        self._ensureConnectionStatus()
        
        command = "AT+GSN"
        
        self.s.write(command + "\r")
        
        if(self.s.readline().strip() == command):
                
            response = self.s.readline().strip()
        
            self.s.readline().strip()   #BLANK
            self.s.readline().strip()   #OK
        
            return response
    
    
    #One-time initial setup function (Disables Flow Control)
    #This only needs to be called once, as is stored in non-volitile memory
    
    #Make sure you DISCONNECT RockBLOCK from power for a few minutes after this command has been issued...
    def setup(self):
        self._ensureConnectionStatus()
        
        
        #Disable Flow Control
        command = "AT&K0"
                
        self.s.write(command + "\r")
        
        if(self.s.readline().strip() == command and self.s.readline().strip() == "OK"):
          
            
            #Store Configuration into Profile0
            command = "AT&W0"
                
            self.s.write(command + "\r")
            
            if(self.s.readline().strip() == command and self.s.readline().strip() == "OK"):
          
            
                #Use Profile0 as default
                command = "AT&Y0"
                    
                self.s.write(command + "\r")
                
                if(self.s.readline().strip() == command and self.s.readline().strip() == "OK"):    
                    
                    
                    #Flush Memory
                    command = "AT*F"
                    
                    self.s.write(command + "\r")
                
                    if(self.s.readline().strip() == command and self.s.readline().strip() == "OK"):
                                                
                        #self.close()
                        
                        return True
                    
        
        
        return False        
    
    def close(self):
        
        if(self.s != None):
            
            self.s.close()
            self.s = None
    
     
    @staticmethod
    def listPorts():
        
        if sys.platform.startswith('win'):
            
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    
            ports = glob.glob('/dev/tty[A-Za-z]*')
    
        elif sys.platform.startswith('darwin'):
    
            ports = glob.glob('/dev/tty.*')
        
        result = []
        
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        
        return result
    
        
    #Private Methods - Don't call these directly!
    def _queueMessage(self, msg):
        self._ensureConnectionStatus()
                
        if( len(msg) > 340):
               
            print("sendMessageWithBytes bytes should be <= 340 bytes")
            
            return False
        
        
        command = "AT+SBDWB=" + str( len(msg) )
        
        self.s.write(command + "\r")
        
        
        if(self.s.readline().strip() == command):
           
            if(self.s.readline().strip() == "READY"):
                
                checksum = 0
                
                for c in msg:
                    
                    checksum = checksum + ord(c)
                
                                
                self.s.write( str(msg) )
                
                self.s.write( chr( checksum >> 8 ) )
                self.s.write( chr( checksum & 0xFF ) )
                                       
                self.s.readline().strip()   #BLANK
                
                result = False
                                
                if(self.s.readline().strip() == "0"):
                
                    result = True
                                                    
                self.s.readline().strip()   #BLANK
                self.s.readline().strip()   #OK
                
                return result
                    
        return False
    
    
    def _configurePort(self):
        
#        if( self._enableEcho() and self._disableFlowControl and self._disableRingAlerts() and self.ping() ):
                        
            return True
        
#        else:
            
#            return False
        
        
    def _enableEcho(self):
        self._ensureConnectionStatus()
        
        command = "ATE1"
        
        self.s.write(command + "\r")
        
        response = self.s.readline().strip()
        
        if(response == command or response == ""):
                 
            if( self.s.readline().strip() == "OK" ):
                
                return True
    
        return False
    
    
    def _disableFlowControl(self):
        self._ensureConnectionStatus()
        
        command = "AT&K0"
        
        self.s.write(command + "\r")
        
        if(self.s.readline().strip() == command):
             
            if( self.s.readline().strip() == "OK" ):
                
                return True
                        
        return False
    
    
    def _disableRingAlerts(self):
        self._ensureConnectionStatus()
                
        command = "AT+SBDMTA=0"
        
        self.s.write(command + "\r")
        
        if( self.s.readline().strip() == command ):
            
            if( self.s.readline().strip() == "OK" ):
                            
                return True
            
        return False
                 
                 
    def _attemptSession(self):
        self._ensureConnectionStatus()
        
        SESSION_ATTEMPTS = 3
                
        while(True):
            
            if(SESSION_ATTEMPTS == 0):
                return False            
            
            SESSION_ATTEMPTS = SESSION_ATTEMPTS - 1
                         
            command = "AT+SBDIX"
            
            self.s.write(command + "\r")
            
            if( self.s.readline().strip() == command ):
                
                response = self.s.readline().strip()
            
                if( response.find("+SBDIX:") >= 0 ):
            
                    self.s.readline()   #BLANK
                    self.s.readline()   #OK
                    
                                    
                    response = response.replace("+SBDIX: ", "")    #+SBDIX:<MO status>,<MOMSN>,<MT status>,<MTMSN>,<MT length>,<MTqueued>
                
                    parts = response.split(",")
                
                    moStatus = int(parts[0])
                    moMsn = int(parts[1])
                    mtStatus = int(parts[2])
                    mtMsn = int(parts[3])
                    mtLength = int(parts[4])
                    mtQueued = int(parts[5])
                    
        
                    #Mobile Originated
                    if(moStatus <= 4):
                        
                        self._clearMoBuffer()
                                            
                        if(self.callback != None and callable(self.callback.rockBlockTxSuccess) ):   
                            self.callback.rockBlockTxSuccess( moMsn )
                        
                        pass
                    
                    else:
                        
                        if(self.callback != None and callable(self.callback.rockBlockTxFailed) ): 
                            self.callback.rockBlockTxFailed()
                    
                    
                    if(mtStatus == 1 and mtLength > 0): #SBD message successfully received from the GSS. 
                        
                        self._processMtMessage(mtMsn)
                    
                    
                    #AUTOGET NEXT MESSAGE
                        
                    if(self.callback != None and callable(self.callback.rockBlockRxMessageQueue) ): 
                        self.callback.rockBlockRxMessageQueue(mtQueued)
                    
                    
                    
                    #There are additional MT messages to queued to download
                    if(mtQueued > 0 and self.autoSession == True):
                        
                        self._attemptSession()
                    
                
                    if(moStatus <= 4):                     
                        return True
                
     
        return False
     
        
    def _attemptConnection(self):
        self._ensureConnectionStatus()

        TIME_ATTEMPTS = 20
        TIME_DELAY = 1
       
        SIGNAL_ATTEMPTS = 10
        RESCAN_DELAY = 10                 
        SIGNAL_THRESHOLD = 2
        
        #Wait for valid Network Time
        while True:
           
            if(TIME_ATTEMPTS == 0):
                
                if(self.callback != None and callable(self.callback.rockBlockSignalFail) ): 
                    self.callback.rockBlockSignalFail()
                
                return False
            
              
            if( self._isNetworkTimeValid() ):
                
                break
                        
            
            TIME_ATTEMPTS = TIME_ATTEMPTS - 1;
            
            time.sleep(TIME_DELAY)
            
                 
        
        #Wait for acceptable signal strength
        while True:
            
            signal = self.requestSignalStrength()
                        
            if(SIGNAL_ATTEMPTS == 0 or signal < 0):
                
                print("NO SIGNAL")
                                
                if(self.callback != None and callable(self.callback.rockBlockSignalFail) ): 
                    self.callback.rockBlockSignalFail()
               
                return False
            
            self.callback.rockBlockSignalUpdate( signal )
            
            if( signal >= SIGNAL_THRESHOLD ):
                
                if(self.callback != None and callable(self.callback.rockBlockSignalPass) ): 
                    self.callback.rockBlockSignalPass()
                                    
                return True;
            
            
            SIGNAL_ATTEMPTS = SIGNAL_ATTEMPTS - 1
            
            time.sleep(RESCAN_DELAY)
        

    def _processMtMessage(self, mtMsn):
        self._ensureConnectionStatus()
        
        self.s.write("AT+SBDRB\r")
        
        response = self.s.readline().strip().replace("AT+SBDRB\r","").strip()
          
        if( response == "OK" ):
        
            print("No message content.. strange!")
            
            if(self.callback != None and callable(self.callback.rockBlockRxReceived) ): 
                self.callback.rockBlockRxReceived(mtMsn, "")
                                    
        else:                                
                                                    
            content = response[2:-2]
                        
            if(self.callback != None and callable(self.callback.rockBlockRxReceived) ): 
                self.callback.rockBlockRxReceived(mtMsn, content)
            
            self.s.readline()   #BLANK?
                
    
    def _isNetworkTimeValid(self):
        self._ensureConnectionStatus()
        
        command = "AT-MSSTM"
        
        self.s.write(command + "\r")
        
        if( self.s.readline().strip() == command ):  #Echo
            
            response = self.s.readline().strip()
        
            if( response.startswith("-MSSTM") ):    #-MSSTM: a5cb42ad / no network service
                
                self.s.readline()   #OK
                self.s.readline()   #BLANK
                                         
                if( len(response) == 16):    
                    
                    return True
                
        
        return False
    
    def _clearMoBuffer(self):
        self._ensureConnectionStatus()
        
        command = "AT+SBDD0"
                
        self.s.write(command + "\r")
          
        if(self.s.readline().strip() == command):
                    
            if(self.s.readline().strip()  == "0"):
                
                self.s.readline()  #BLANK
                                              
                if(self.s.readline().strip() == "OK"):
                    
                    return True
                        
        return False
        
    def _ensureConnectionStatus(self):
        
        if(self.s == None or self.s.isOpen() == False):
            
            raise rockBlockException()
        
################################################################################
################################################################################
	




################################################################################
################################################################################
# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Modified by E.Sousa to run on the RPi
#	-Comment out 'from micropython import const'
#	-Change _GPSI2C_DEFAULT_ADDRESS = const(0x10)
#	   to   _GPSI2C_DEFAULT_ADDRESS = 0x10
"""
`adafruit_gps`
====================================================

GPS parsing module.  Can parse simple NMEA data sentences from serial GPS
modules to read latitude, longitude, and more.

* Author(s): Tony DiCola

Implementation Notes
--------------------

**Hardware:**

* Adafruit `Ultimate GPS Breakout <https://www.adafruit.com/product/746>`_
* Adafruit `Ultimate GPS FeatherWing <https://www.adafruit.com/product/3133>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases

"""
import time
#from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_GPS.git"


#_GPSI2C_DEFAULT_ADDRESS = const(0x10)
_GPSI2C_DEFAULT_ADDRESS = 0x10

# Internal helper parsing functions.
# These handle input that might be none or null and return none instead of
# throwing errors.
def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes / 60


def _parse_int(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return int(nmea_data)


def _parse_float(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return float(nmea_data)


def _parse_str(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return str(nmea_data)


# lint warning about too many attributes disabled
# pylint: disable-msg=R0902


class GPS:
    """GPS parsing module.  Can parse simple NMEA data sentences from serial
    GPS modules to read latitude, longitude, and more.
    """

    def __init__(self, uart, debug=False):
        self._uart = uart
        # Initialize null starting values for GPS attributes.
        self.timestamp_utc = None
        self.latitude = None
        self.longitude = None
        self.fix_quality = None
        self.fix_quality_3d = None
        self.satellites = None
        self.satellites_prev = None
        self.horizontal_dilution = None
        self.altitude_m = None
        self.height_geoid = None
        self.speed_knots = None
        self.track_angle_deg = None
        self.sats = None
        self.isactivedata = None
        self.true_track = None
        self.mag_track = None
        self.sat_prns = None
        self.sel_mode = None
        self.pdop = None
        self.hdop = None
        self.vdop = None
        self.total_mess_num = None
        self.mess_num = None
        self._raw_sentence = None
        self.debug = debug

    def update(self):
        """Check for updated data from the GPS module and process it
        accordingly.  Returns True if new data was processed, and False if
        nothing new was received.
        """
        # Grab a sentence and check its data type to call the appropriate
        # parsing function.
        try:
            sentence = self._parse_sentence()
        except UnicodeError:
            return None
        if sentence is None:
            return False
        if self.debug:
            print(sentence)
        data_type, args = sentence
#        data_type = bytes(data_type.upper(), "ascii") #for python3
        data_type = bytes(data_type.upper()) #for python2
        # return sentence
        if data_type in (b"GPGLL", b"GNGLL"):  # GLL, Geographic Positition Latitude/Longitude
            self._parse_gpgll(args)
        elif data_type in (b"GPRMC", b"GNRMC"):  # RMC, minimum location info
            self._parse_gprmc(args)
        elif data_type in (b"GPGGA", b"GNGGA"):  # GGA, 3d location fix
            self._parse_gpgga(args)
        return True

    def send_command(self, command, add_checksum=True):
        """Send a command string to the GPS.  If add_checksum is True (the
        default) a NMEA checksum will automatically be computed and added.
        Note you should NOT add the leading $ and trailing * to the command
        as they will automatically be added!
        """
        self.write(b"$")
        self.write(command)
        if add_checksum:
            checksum = 0
            for char in command:
                checksum ^= char
            self.write(b"*")
            self.write(bytes("{:02x}".format(checksum).upper(), "ascii"))
        self.write(b"\r\n")

    @property
    def has_fix(self):
        """True if a current fix for location information is available."""
        return self.fix_quality is not None and self.fix_quality >= 1

    @property
    def has_3d_fix(self):
        """Returns true if there is a 3d fix available.
        use has_fix to determine if a 2d fix is available,
        passing it the same data"""
        return self.fix_quality_3d is not None and self.fix_quality_3d >= 2

    @property
    def datetime(self):
        """Return struct_time object to feed rtc.set_time_source() function"""
        return self.timestamp_utc

    @property
    def nmea_sentence(self):
        """Return raw_sentence which is the raw NMEA sentence read from the GPS"""
        return self._raw_sentence

    def read(self, num_bytes):
        """Read up to num_bytes of data from the GPS directly, without parsing.
        Returns a bytearray with up to num_bytes or None if nothing was read"""
        return self._uart.read(num_bytes)

    def write(self, bytestr):
        """Write a bytestring data to the GPS directly, without parsing
        or checksums"""
        return self._uart.write(bytestr)

    @property
    def in_waiting(self):
        """Returns number of bytes available in UART read buffer"""
        return self._uart.in_waiting

    def readline(self):
        """Returns a newline terminated bytearray, must have timeout set for
        the underlying UART or this will block forever!"""
        return self._uart.readline()

    def _read_sentence(self):
        # Parse any NMEA sentence that is available.
        # pylint: disable=len-as-condition
        # This needs to be refactored when it can be tested.

        # Only continue if we have at least 32 bytes in the input buffer
        if self.in_waiting < 32:
            return None

        sentence = self.readline()
        if sentence is None or sentence == b"" or len(sentence) < 1:
            return None
        try:
#            sentence = str(sentence, "ascii").strip() #for python3
            sentence = str(sentence).strip() #for python2
        except UnicodeError:
            return None
        # Look for a checksum and validate it if present.
        if len(sentence) > 7 and sentence[-3] == "*":
            # Get included checksum, then calculate it and compare.
            expected = int(sentence[-2:], 16)
            actual = 0
            for i in range(1, len(sentence) - 3):
                actual ^= ord(sentence[i])
            if actual != expected:
                return None  # Failed to validate checksum.

            # copy the raw sentence
            self._raw_sentence = sentence

            return sentence
        # At this point we don't have a valid sentence
        return None

    def _parse_sentence(self):
        sentence = self._read_sentence()

        # sentence is a valid NMEA with a valid checksum
        if sentence is None:
            return None

        # Remove checksum once validated.
        sentence = sentence[:-3]
        # Parse out the type of sentence (first string after $ up to comma)
        # and then grab the rest as data within the sentence.
        delimiter = sentence.find(",")
        if delimiter == -1:
            return None  # Invalid sentence, no comma after data type.
        data_type = sentence[1:delimiter]
        return (data_type, sentence[delimiter + 1 :])

    def _parse_gpgll(self, args):
        data = args.split(",")
        if data is None or data[0] is None:
            return  # Unexpected number of params.

        # Parse latitude and longitude.
        self.latitude = _parse_degrees(data[0])
        if self.latitude is not None and data[1] is not None and data[1].lower() == "s":
            self.latitude *= -1.0
        self.longitude = _parse_degrees(data[2])
        if (
            self.longitude is not None
            and data[3] is not None
            and data[3].lower() == "w"
        ):
            self.longitude *= -1.0
        time_utc = int(_parse_int(float(data[4])))
        if time_utc is not None:
            hours = time_utc // 10000
            mins = (time_utc // 100) % 100
            secs = time_utc % 100
            # Set or update time to a friendly python time struct.
            if self.timestamp_utc is not None:
                self.timestamp_utc = time.struct_time(
                    (0, 0, 0, hours, mins, secs, 0, 0, -1)
                )
            else:
                self.timestamp_utc = time.struct_time(
                    (0, 0, 0, hours, mins, secs, 0, 0, -1)
                )
        # Parse data active or void
        self.isactivedata = _parse_str(data[5])

    def _parse_gprmc(self, args):
        # Parse the arguments (everything after data type) for NMEA GPRMC
        # minimum location fix sentence.
        data = args.split(",")
        if data is None or len(data) < 11 or data[0] is None:
            return  # Unexpected number of params.
        # Parse fix time.
        time_utc = int(_parse_float(data[0]))
        if time_utc is not None:
            hours = time_utc // 10000
            mins = (time_utc // 100) % 100
            secs = time_utc % 100
            # Set or update time to a friendly python time struct.
            if self.timestamp_utc is not None:
                self.timestamp_utc = time.struct_time(
                    (
                        self.timestamp_utc.tm_year,
                        self.timestamp_utc.tm_mon,
                        self.timestamp_utc.tm_mday,
                        hours,
                        mins,
                        secs,
                        0,
                        0,
                        -1,
                    )
                )
            else:
                self.timestamp_utc = time.struct_time(
                    (0, 0, 0, hours, mins, secs, 0, 0, -1)
                )
        # Parse status (active/fixed or void).
        status = data[1]
        self.fix_quality = 0
        if status is not None and status.lower() == "a":
            self.fix_quality = 1
        # Parse latitude and longitude.
        self.latitude = _parse_degrees(data[2])
        if self.latitude is not None and data[3] is not None and data[3].lower() == "s":
            self.latitude *= -1.0
        self.longitude = _parse_degrees(data[4])
        if (
            self.longitude is not None
            and data[5] is not None
            and data[5].lower() == "w"
        ):
            self.longitude *= -1.0
        # Parse out speed and other simple numeric values.
        self.speed_knots = _parse_float(data[6])
        self.track_angle_deg = _parse_float(data[7])
        # Parse date.
        if data[8] is not None and len(data[8]) == 6:
            day = int(data[8][0:2])
            month = int(data[8][2:4])
            year = 2000 + int(data[8][4:6])  # Y2k bug, 2 digit year assumption.
            # This is a problem with the NMEA
            # spec and not this code.
            if self.timestamp_utc is not None:
                # Replace the timestamp with an updated one.
                # (struct_time is immutable and can't be changed in place)
                self.timestamp_utc = time.struct_time(
                    (
                        year,
                        month,
                        day,
                        self.timestamp_utc.tm_hour,
                        self.timestamp_utc.tm_min,
                        self.timestamp_utc.tm_sec,
                        0,
                        0,
                        -1,
                    )
                )
            else:
                # Time hasn't been set so create it.
                self.timestamp_utc = time.struct_time(
                    (year, month, day, 0, 0, 0, 0, 0, -1)
                )

    def _parse_gpgga(self, args):
        # Parse the arguments (everything after data type) for NMEA GPGGA
        # 3D location fix sentence.
        data = args.split(",")
        if data is None or len(data) != 14:
            return  # Unexpected number of params.
        # Parse fix time.
        time_utc = int(_parse_float(data[0]))
        if time_utc is not None:
            hours = time_utc // 10000
            mins = (time_utc // 100) % 100
            secs = time_utc % 100
            # Set or update time to a friendly python time struct.
            if self.timestamp_utc is not None:
                self.timestamp_utc = time.struct_time(
                    (
                        self.timestamp_utc.tm_year,
                        self.timestamp_utc.tm_mon,
                        self.timestamp_utc.tm_mday,
                        hours,
                        mins,
                        secs,
                        0,
                        0,
                        -1,
                    )
                )
            else:
                self.timestamp_utc = time.struct_time(
                    (0, 0, 0, hours, mins, secs, 0, 0, -1)
                )
        # Parse latitude and longitude.
        self.latitude = _parse_degrees(data[1])
        if self.latitude is not None and data[2] is not None and data[2].lower() == "s":
            self.latitude *= -1.0
        self.longitude = _parse_degrees(data[3])
        if (
            self.longitude is not None
            and data[4] is not None
            and data[4].lower() == "w"
        ):
            self.longitude *= -1.0
        # Parse out fix quality and other simple numeric values.
        self.fix_quality = _parse_int(data[5])
        self.satellites = _parse_int(data[6])
        self.horizontal_dilution = _parse_float(data[7])
        self.altitude_m = _parse_float(data[8])
        self.height_geoid = _parse_float(data[10])

    def _parse_gpgsa(self, args):
        data = args.split(",")
        if data is None:
            return  # Unexpected number of params

        # Parse selection mode
        self.sel_mode = _parse_str(data[0])
        # Parse 3d fix
        self.fix_quality_3d = _parse_int(data[1])
        satlist = list(filter(None, data[2:-4]))
        self.sat_prns = {}
        for i, sat in enumerate(satlist, 1):
            self.sat_prns["gps{}".format(i)] = _parse_int(sat)

        # Parse PDOP, dilution of precision
        self.pdop = _parse_float(data[-3])
        # Parse HDOP, horizontal dilution of precision
        self.hdop = _parse_float(data[-2])
        # Parse VDOP, vertical dilution of precision
        self.vdop = _parse_float(data[-1])

    def _parse_gpgsv(self, args):
        # Parse the arguments (everything after data type) for NMEA GPGGA
        # 3D location fix sentence.
        data = args.split(",")
        if data is None:
            return  # Unexpected number of params.

        # Parse number of messages
        self.total_mess_num = _parse_int(data[0])  # Total number of messages
        # Parse message number
        self.mess_num = _parse_int(data[1])  # Message number
        # Parse number of satellites in view
        self.satellites = _parse_int(data[2])  # Number of satellites

        if len(data) < 3:
            return

        sat_tup = data[3:]

        satdict = {}
        for i in range(len(sat_tup) / 4):
            j = i * 4
            key = "gps{}".format(i + (4 * (self.mess_num - 1)))
            satnum = _parse_int(sat_tup[0 + j])  # Satellite number
            satdeg = _parse_int(sat_tup[1 + j])  # Elevation in degrees
            satazim = _parse_int(sat_tup[2 + j])  # Azimuth in degrees
            satsnr = _parse_int(sat_tup[3 + j])  # signal-to-noise ratio in dB
            value = (satnum, satdeg, satazim, satsnr)
            satdict[key] = value

        if self.sats is None:
            self.sats = {}
        for satnum in satdict:
            self.sats[satnum] = satdict[satnum]

        try:
            if self.satellites < self.satellites_prev:
                for i in self.sats:
                    try:
                        if int(i[-2]) >= self.satellites:
                            del self.sats[i]
                    except ValueError:
                        if int(i[-1]) >= self.satellites:
                            del self.sats[i]
        except TypeError:
            pass
        self.satellites_prev = self.satellites
