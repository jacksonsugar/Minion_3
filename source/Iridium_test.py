import minsat
from minsat import MinSat
import sys, os
import subprocess

addrs = subprocess.Popen(['i2cdetect','-y','1'],stdout=subprocess.PIPE,)

for i in range(0,9):
    line = str(addrs.stdout.readline())

    if "49" not in line:
        print("Iridium Modem not connected!")
        exit(1)

gps_port = "/dev/ttySC0"
gps_baud = 9600
modem_port = "/dev/ttySC1"
modem_baud = 19200

m1 = MinSat(gps_port,gps_baud,modem_port,modem_baud)

def display_gps_resp_struct(ret_info):
    print(
        "Successful Fix: {}/{}/{} {:02}:{:02}:{:02} -- {:.6f},{:06f}".format(
            ret_info.tm_mon,  # Grab parts of the time from the
            ret_info.tm_mday,  # struct_time object that holds
            ret_info.tm_year,  # the fix time.  Note you might
            ret_info.tm_hour,  # not get all data like year, day,
            ret_info.tm_min,  # month!
            ret_info.tm_sec,
            ret_info.latitude,
            ret_info.longitude,
        )
    )



(okay,ret_data) = m1.sbd_send_position(verbose=False,maintain_gps_pwr=True,gps_timeout=120)

if okay and ret_data.valid_position:

    display_gps_resp_struct(ret_data)

elif not okay and  not ret_data.valid_position:
    print("Could not acquire a valid GPS Position.")

elif not okay and ret_data.valid_position:
    print("Valid GPS Position Acquired - Could Not Transmit the Position via Irdium.")

m1.gps_pwr(m1.dev_off)
