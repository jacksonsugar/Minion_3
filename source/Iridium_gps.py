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


(okay,ret_data) = m1.sbd_send_position(verbose=False,maintain_gps_pwr=True,gps_timeout=120)

if okay and ret_data.valid_position:
    print("Valid GPS Position Acquired & Transmitted via Iridium.")
    display_gps_resp_struct(ret_data)
elif not okay and  not ret_data.valid_position:
    print("Could not acquire a valid GPS Position.")
    print("Second Attempt")
    (okay,ret_data) = m1.sbd_send_position(verbose=False,maintain_gps_pwr=True,gps_timeout=120)
elif not okay and ret_data.valid_position:
    print("Valid GPS Position Acquired - Could Not Transmit the Position via Irdium.")
    display_gps_resp_struct(ret_data)
    print("Second Attempt")
    (okay,ret_data) = m1.sbd_send_position(verbose=False,maintain_gps_pwr=True,gps_timeout=120)
    
m1.gps_pwr(m1.dev_off)