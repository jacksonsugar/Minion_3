#!/usr/bin/env python

import os
import pickle

countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","wb")
sampcount = 0
pickle.dump(sampcount, countp)
countp.close()

os.system('sudo rm -r /home/pi/Desktop/minion_pics/*')
os.system('sudo rm -r /home/pi/Desktop/minion_data/*.txt')
os.system('sudo rm -r /home/pi/Desktop/minion_data/INI/*')
os.system('sudo rm -r /home/pi/Desktop/minion_data/FIN/*')

print('Minion Data Cleared!')

