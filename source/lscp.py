import os
import sys
import time

cwd = os.getcwd()

usrHome = str(os.path.expanduser("~"))

def yes_no(answer):
    yes = set(['yes','y', 'ye', 'yeet', ''])
    no = set(['no','n'])

    while True:
        choice = raw_input(answer).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'\n")

def mkdir_safe(path):
	if os.path.isdir(path) == True:
		print("\nDirectory: [{}] already exists. \n\nProcess stopped to protect files.".format(path))
		exit(0)

	elif os.path.isdir(path) == False:
		os.system("mkdir {}".format(path))

	else:
		print("Mistakes were made here")
		exit(0)


# to simplify the {scp remote_username@10.10.0.2:/remote/file.txt /local/directory}
try:
    numMinion = sys.argv[1]

except:
    numMinion = ''

try:
    dataType = str(sys.argv[2])

except:
    dataType = ''

if numMinion == '':
    print(numMinion)
    print('No file specified in argument. Please use form: lscp [Minion Number]')
    exit(0)

if numMinion == '-h':

    print('This script is designed to be used remotely from the MINION')
    print('Execute this local script to retrieve data from a remote host\n')
    print('Use the form: lscp [Minion_Number] [pics/data/both]\n')
    print('If pics or data not determined both are copied to \n the local specified destination.')
    exit(0)

numMinion = int(numMinion)

hostMinion = 'pi@192.168.0.{}'.format(numMinion)

HOST_UP  = True if os.system("ping -c 1 -W 1 192.168.0.{}".format(numMinion)) is 0 else False

if HOST_UP == False:
    print('Minion [{}] not connected to WIFI'.format(numMinion))
    exit(0)

Destination = yes_no('Do you wish to save files to {}/Desktop/? [Y/N] : '.format(usrHome))

if Destination == False:
    Destination = raw_input("Please specify local file destination: {}/".format(usrHome))
    Destination = Destination.strip("/")
    Destination = "{}/{}/Minion_{}".format(usrHome, Destination, numMinion)
    mkdir_safe(Destination)

else:
    Destination = '{}/Desktop/Minion_{}'.format(usrHome,numMinion)
    mkdir_safe(Destination)


if dataType == 'custom':
    customFile = raw_input("Please input specific file location:  /")
    os.system('sudo scp -r {}:/{} {}'.format(hostMinion, customFile, Destination))

elif dataType == 'pics':
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_pics/ {}'.format(hostMinion, Destination))

elif dataType == 'data':
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_data/ {}'.format(hostMinion, Destination))

elif dataType == '' or 'both':
    os.system('sudo scp -r -T {}:"/home/pi/Desktop/minion_pics/ /home/pi/Desktop/minion_data/" "{}"'.format(hostMinion, Destination))
#    os.system('sudo scp -r {}:/home/pi/Desktop/minion_data/ {}/'.format(hostMinion, Destination))

else:
    print('Please specify either [pics] or [data]')

print('\nData copied successfully!\n - {}'.format(Destination))