import os, sys
import subprocess


nmap = "sudo nmap -sP 192.168.0.1/24"

ssid = "iwgetid"

hub = os.popen(ssid).read()

hub = hub.split('"')[1::2]

print("Devices attached to the {}:\r\n\r\n".format(hub[0]))

scan = os.popen(nmap).read()

for line in scan.split('Nmap scan '):
    if " 192.168.0." in line and "Raspberry Pi" in line:
        line = line.strip("report for ")
        line = line.split("\n")
        IPs = line[0]
        print("Minion @ {}\r\n".format(IPs))

