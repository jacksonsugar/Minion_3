import minsat
from minsat import MinSat
import time


ex_msg = "Example 17 - Powering the Iridium Modem On and Off"

print("-"*len(ex_msg))
print(ex_msg)
print("-"*len(ex_msg))

gps_port = "/dev/ttySC0"
gps_baud = 9600
modem_port = "/dev/ttySC1"
modem_baud = 19200

m1 = MinSat(gps_port,gps_baud,modem_port,modem_baud)

num_secs = 5

m1.modem_pwr(m1.dev_on)
print("Iridium Modem Power On.")
print("Waiting for " + str(num_secs) + " seconds...")
time.sleep(num_secs)
m1.modem_pwr(m1.dev_off)
print("Iridium Modem Power Off.")




