import minsat
from minsat import MinSat
import time
import random

file = "/home/pi/Snocam_data/Finaldata.txt"
sent_entire_file = False
new_file_position = 0

gps_port = "/dev/ttySC0"
gps_baud = 9600
modem_port = "/dev/ttySC1"
modem_baud = 19200

m1 = MinSat(gps_port,gps_baud,modem_port,modem_baud)

def display_sbd_resp_struct(resp_struct):
    print("=" * 50)
    print("File Name: " + str(resp_struct.file_name))
    print("File Open Success: " + str(resp_struct.file_open_success))
    print("File Size: " + str(resp_struct.file_size))
    print("File Position Starting Point: " + str(resp_struct.start_file_loc))
    print("Number of SBD Sessions Required: " +str(resp_struct.xmt_num_sbd_req))
    print("Number of SBD Sessions Successfully Transmitted: " + str(resp_struct.xmt_num_sbd_success))
    print("Completed Sending File: " + str(resp_struct.xmt_file_complete))
    print("Number of Bytes Transmitted: " + str(resp_struct.xmt_num_bytes)) #Note that the transmitted number of bytes can be larger than the file size if num_hearder_lines > 0
    print("Current File Location: " + str(resp_struct.curr_file_loc))

while sent_entire_file == False:
    ret_info = m1.sbd_send_file(file,verbose=False,num_header_lines=1,start_file_position=new_file_position,ird_sig_timeout=60)
    sent_entire_file = ret_info.xmt_file_complete
    new_file_position = ret_info.curr_file_loc
    if sent_entire_file == False:
        m1.modem_pwr(m1.dev_off)
        print("File partially sent, sending next batch.")
        time.sleep(5)
        
display_sbd_resp_struct(ret_info)





