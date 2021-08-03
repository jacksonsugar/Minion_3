import os, sys
import subprocess

IPs = []

nmap = "sudo nmap -sP 192.168.0.1/24"

ssid = "iwgetid"

devs = False

hub = os.popen(ssid).read()

hub = hub.split('"')[1::2]

scan = os.popen(nmap).read()

for line in scan.split('Nmap scan '):
    if " 192.168.0." in line and "Raspberry Pi" in line:
        devs = True
        line = line.strip("report for ")
        line = line.split("\n")
        IPs.append(line[0])
        print("Minion @ {}\r\n".format(IPs))

output = ''.join(IPs)

if devs == True:
    print("Devices attached to the {}:\r\n\r\n".format(hub[0]))

    print(output)

else:
    print("No other devices attached to the {}.".format(hub[0]))
