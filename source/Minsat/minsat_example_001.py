import minsat
from minsat import MinSat

ex_msg = "Example 1 - Sending a message via Iridium when the message is 340 bytes or less"

print("-"*len(ex_msg))
print(ex_msg)
print("-"*len(ex_msg))

gps_port = "/dev/ttySC0"
gps_baud = 9600
modem_port = "/dev/ttySC1"
modem_baud = 19200

m1 = MinSat(gps_port,gps_baud,modem_port,modem_baud)

message1 = "Listen. Strange women lying in ponds distributing swords is no basis for a system of government. Supreme executive power derives from a mandate from the masses, not from some farcical aquatic ceremony."

resp = m1.sbd_send_message(message1)
print("resp = " + str(resp))
