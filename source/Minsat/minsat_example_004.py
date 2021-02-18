import minsat
from minsat import MinSat

ex_msg = "Example 4 - Acquiring a GPS Position with enhanced verbosity"

print("-"*len(ex_msg))
print(ex_msg)
print("-"*len(ex_msg))

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

