from zipfile import ZipFile
import os
import time
import sys

data = sys.argv[1]

if data == False:
    exit(0)

path = '/home/pi/Desktop/minion_memory/{}'.format(data)

def get_all_files(directory):

    paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root,filename)
            paths.append(filepath)

    return paths

def clear_log():
    output = open('/var/www/html/livefeed.txt','w')
    output.write('')
    output.close()

endmessage = "Files Compressed!"

clear_log()

zipname = "/var/www/html/MXXX-{}.zip".format(data)

paths = get_all_files(path)

with ZipFile(zipname,'w') as zip:
    for file in paths:
        filename = file.replace('/home/pi/Desktop/minion_memory','')
        zip.write(file, filename)
        output = open('/var/www/html/livefeed.txt','a+')
        output.write(file)
        output.write('<br><br>')
        output.close()

output = open('/var/www/html/livefeed.txt','w')
output.write(endmessage)
output.write("<br><br>")
output.close()

time.sleep(10)

clear_log()
