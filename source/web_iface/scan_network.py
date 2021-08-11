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
        print("Minion @ <a target='_blank' rel='noopener noreferrer' href='http://{}/index.php'>{}</a>\r\n".format(line[0],line[0]))

if devs == True:
    print("On the {}!\r\n".format(hub[0]))

else:
    print("No other devices attached to the {}.".format(hub[0]))


