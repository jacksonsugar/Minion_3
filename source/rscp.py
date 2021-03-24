import os
import sys
import time

cwd = os.getcwd()

print(cwd)

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

# to simplify the { sudo scp -r *Stuff* *remoteuser*:*Location*}
try:
	file2send = sys.argv[1]
#	if '/' in file2send:
#		file2send = file2send.replace('/','')

except:
	file2send = ''

if file2send == '':
	print(file2send)
	print('No file specified in argument. Please use form: rscp [file/directory]')
	exit(0)

if file2send == '-h':

	print('This script is designed to live locally on the MINION.')
	print('Execute this local script from a remote ssh device to scp selected data back.')
	print('Use the form: rscp [file/directory]')
	exit(0)

cwd = (cwd + "/")

file2send = cwd + file2send

print('File to send: ' + file2send)

returnADDR = os.popen('w').read()
returnADDR = returnADDR.split('\n')

if returnADDR[3] == '':
	print('No SSH device connected')
	exit(0)

Host = returnADDR[3].split(' ')

while("" in Host):
    Host.remove("")

HostUsr = raw_input("Remote computer's username:")
HostIP = Host[2]

HostStr = "{}@{}".format(HostUsr, HostIP)

Destination = yes_no('Do you wish to save files to {}:/home/{}/Desktop/? [Y/N] : '.format(HostStr, HostUsr))

if Destination == False:
    Destination = raw_input("Please specify local file destination: /home/{}/".format(HostUsr))
    Destination = "/home/{}/{}".format(HostUsr, Destination)

else:
    Destination = '/home/{}/Desktop/'.format(HostUsr)

print('Files will be copied to remote user {}:{}'.format(HostUsr, Destination))

secureCopy = 'sudo scp -r {} {}:{}'.format(file2send, HostStr, Destination)

print(secureCopy)

os.system(secureCopy)
