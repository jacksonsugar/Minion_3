#!/usr/bin/env python

import os

os.system('sudo rm -r /home/pi/Desktop/minion_pics/*')
os.system('sudo rm -r /home/pi/Desktop/minion_data/*.txt')
os.system('sudo rm -r /home/pi/Desktop/minion_data/INI/*')
os.system('sudo rm -r /home/pi/Desktop/minion_data/FIN/*')

print('Minion Data Cleared!')

