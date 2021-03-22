import os
import sys
import time

cwd = os.getcwd()

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


# to simplify the {scp remote_username@10.10.0.2:/remote/file.txt /local/directory}
try:
    numMinion = int(sys.argv[1])

except:
    numMinion = ''

try:
    dataType = int(sys.argv[2])

except:
    dataType = ''

if numMinion == '':
    print(numMinion)
    print('No file specified in argument. Please use form: rscp [file/directory] [pics/data]')
    exit(0)

if numMinion == '-h':
    
    print('This script is designed to be used remotely from the MINION')
    print('Execute this local script to retrieve data from a remote host')
    print('Use the form: rscp [Minion_Number] [pics/data]')
    print('If pics or data not determined both are copied to \n the local specified destination.')
    exit(0)

hostMinion = 'pi@192.168.0.{}'.format(numMinion)

HOST_UP  = True if os.system("ping -c 1 -W 1 192.168.0.{}".format(numMinion)) is 0 else False

if HOST_UP == False:
    print('Minion [{}] not connected to WIFI'.format(numMinion))
    exit(0)

print(numMinion)

Destination = yes_no('Do you wish to save files locally to ~/Desktop/? [Y/N]')

if Destination == False:
    Destination = raw_input("Please specify local file destination: ")

else:
    os.mkdir('~/Desktop/Minion_{}'.format(numMinion))
    Destination = '~/Desktop/Minion_{}'.format(numMinion)

if dataType == '':
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_pics/ {}'.format(hostMinion, Destination))
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_data/ {}'.format(hostMinion, Destination))

if dataType == 'pics':
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_pics/ {}'.format(hostMinion, Destination))

if dataType == 'data':
    os.system('sudo scp -r {}:/home/pi/Desktop/minion_data/ {}'.format(hostMinion, Destination))

else:
    print('Please specify either [pics] or [data]')