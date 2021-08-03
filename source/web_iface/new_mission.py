import os
import pickle

countp = open("/home/pi/Documents/Minion_scripts/sampcount.pkl","wb")
sampcount = 0
pickle.dump(sampcount, countp)
countp.close()

time = os.popen('ls /home/pi/Desktop/minion_data/INI/1-*.txt').read()

time = time.strip('/home/pi/Desktop/minion_data/INI/1-')

time = time.strip('_TEMPPRES-INI.txt\n')

num_mem = int(len(os.listdir('/home/pi/Desktop/minion_memory/'))) + 1

save_dir = '/home/pi/Desktop/minion_memory/{}-{}'.format(num_mem, time)

os.system('sudo mkdir {}'.format(save_dir))

os.system('sudo mv /home/pi/Desktop/minion_data/ /home/pi/Desktop/minion_pics/ {}'.format(save_dir))

os.system('sudo cp /home/pi/Desktop/Minion_config.ini {}'.format(save_dir))

os.system('sudo mkdir /home/pi/Desktop/minion_data/ /home/pi/Desktop/minion_pics/')

os.system('sudo mkdir /home/pi/Desktop/minion_data/INI/ /home/pi/Desktop/minion_data/FIN/')

dir_name = save_dir.strip('/home/pi/Desktop/minion_memory/')

print('Files are saved to {}'.format(dir_name))
