#!/usr/bin/env python

'''
This program was written to simplify configuration of a
Minion camera/sensor/vehicle.

More tools to be added in future versions

'''
import RPi.GPIO as GPIO
import time
import os

print("Welcome to the Minion installer 3! \n")

ini_dir = os.getcwd()

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

def USB_Conf():

    drive = raw_input('Please insert USB storage device and press return:')
    # Below formats the Drive automatically but wow it's slow
    #os.system('sudo mkfs -t ntfs /dev/sda1')

    drives = os.popen("sudo blkid").read()

    drives = drives.splitlines()

    not_drive = []

    for i in [i for i,x in enumerate(drives) if x.find('mmc') != -1]:
        not_drive.append(i)

    for i in [i for i,x in enumerate(drives) if x.find('loop') != -1]:
        not_drive.append(i)

    drives = [i for j, i in enumerate(drives) if j not in not_drive]

    drive = drives[0]

    drive = drive.split(':')[0]

    print(drive)

    UUID = os.popen('sudo blkid -o value /dev/sda1').read().splitlines()[3]

    print(UUID)

    return UUID

# Configure the last 3 digits of IP 192.168.0.XXX

IP_addr = input('What local IP extension would you like to use? 192.168.0.')

if len(str(IP_addr)) > 3 or len(str(IP_addr)) < 1 or IP_addr <= 1 or IP_addr >= 255:
    IP_fail = 1
    while IP_fail == 1: 
        IP_addr = input('Illigal IP address: 192.168.0.%s! Please try again: ' % IP_addr)
        if len(str(IP_addr)) > 3 or len(str(IP_addr)) < 1 or IP_addr <= 1 or IP_addr >= 255:
            pass
        else:
            IP_fail = 0
            print("Local IP address = 192.168.0.%s" % IP_addr)
else:
    print("Minion_Hub IP address = 192.168.0.%s" % IP_addr)

# Write to /etc/dhcpcd.Minion file

os.system('sudo cp source/dhcp/dhcpcd.conf source/dhcp/dhcpcd.Minion /etc/')

# Open dhcpcd.Minion
with open('/etc/dhcpcd.Minion', 'r') as file :
    Minion_dhcp = file.read()

# Replace the IP string
Minion_dhcp = Minion_dhcp.replace('XXX', str(IP_addr))

# Write the file out again
with open('/etc/dhcpcd.Minion', 'w') as file:
    file.write(Minion_dhcp)
  
# Set up wifi

os.system("sudo sh -c 'cat source/dhcp/wpa_supplicant.txt >> /etc/wpa_supplicant/wpa_supplicant.conf'")

# Enable the splash screen easter egg
    
Debug = yes_no('Do you want to enable debug mode? [Y/N] : ')

os.system('sudo mv /usr/share/plymouth/themes/pix/splash.png /usr/share/plymouth/themes/pix/splash.png.old')
os.system('sudo cp source/splash.png /usr/share/plymouth/themes/pix/')

if Debug == True:
    os.system("sudo raspi-config nonint do_boot_splash 1")
elif Debug == False:
    os.system("sudo raspi-config nonint do_boot_splash 0")
else:
    print("WTH did you do??")

USBdata = yes_no('Do you wish to configure a USB storage device? (NTFS file system) [Y/N]: ')
os.system('sudo mkdir /home/pi/Documents/Minion_scripts /home/pi/Documents/Minion_tools')
# Move the deployment handler so it knows where to look for config file
os.system('sudo cp source/Data_config.ini source/Minion_DeploymentHandler.py source/Gelcam_DeploymentHandler.py source/Minion_image.py source/Extended_Sampler.py source/Recovery_Sampler_Burn.py source/Recovery_Sampler.py source/OXYBASE_RS232.py source/TempPres.py source/ACC_100Hz.py source/ACC_100Hz_IF.py source/Minion_image_IF.py source/OXYBASE_RS232_IF.py source/minsat.py source/Minsat/SC16IS752GPIO.so source/Iridium_gps.py source/Iridium_data.py source/Temperature_test.py source/Pressure_test.py /home/pi/Documents/Minion_scripts')

if USBdata == True:

    # Mount SD card for use
    os.system("sudo mkdir /media/Data")

    UUID = USB_Conf()

    print(UUID)

    while UUID != os.popen('sudo blkid -o value /dev/sda1').read().splitlines()[3]:
        USB_Conf()

    os.system("sudo sed -i -e '$a PARTUUID=%s /media/Data      ntfs   defaults  0  0' /etc/fstab" % UUID)

    os.system('sudo mount -a')

    print("All files for operation found inside /media/Data on USB drive!")
    
    time.sleep(3)

    os.system('sudo mkdir /media/Data/minion_pics /media/Data/minion_data')
    os.system('sudo mkdir /media/Data/minion_data/INI /media/Data/minion_data/FIN')

    os.system('sudo cp source/Minion_config.ini /media/Data/')

    # Add IP address to config file
    with open('/media/Data/Minion_config.ini', 'r') as file :
        Minion_conf = file.read()

    # Replace the directory
    Minion_conf = Minion_conf.replace('XXX', '{}'.format(IP_addr))

    # Write the file out again
    with open('/media/Data/Minion_config.ini', 'w') as file:
        file.write(Minion_conf)

    os.system("echo '# Minion IP:192.168.0.{}' >> /media/Data/Minion_config.ini".format(IP_addr))

    # Open Minion config file
    with open('/home/pi/Documents/Minion_scripts/Data_config.ini', 'r') as file :
        Minion_conf = file.read()

    # Replace the directory
    Minion_conf = Minion_conf.replace('/home/pi/Desktop', '/media/Data')

    # Write the file out again
    with open('/home/pi/Documents/Minion_scripts/Data_config.ini', 'w') as file:
        file.write(Minion_conf)

elif USBdata == False:

    print("All files for operation found inside /home/pi/Desktop!")
    os.system('sudo mkdir /home/pi/Desktop/minion_pics /home/pi/Desktop/minion_data')
    os.system('sudo mkdir  /home/pi/Desktop/minion_data/INI /home/pi/Desktop/minion_data/FIN')
    os.system('sudo cp source/Minion_config.ini /home/pi/Desktop')

    # Add IP address to config file
    with open('/home/pi/Desktop/Minion_config.ini', 'r') as file :
        Minion_conf = file.read()

    # Replace the directory
    Minion_conf = Minion_conf.replace('XXX', '{}'.format(IP_addr))

    # Write the file out again
    with open('/home/pi/Desktop/Minion_config.ini', 'w') as file:
        file.write(Minion_conf)

    time.sleep(3)
    os.system("echo '# Minion IP:192.168.0.{}' >> /home/pi/Desktop/Minion_config.ini".format(IP_addr))


else:

    print('How did you do this..')

# Set up external software and raspi-config
# Get updates
#os.system('sudo apt-get update && sudo apt-get upgrade -y') 
# Get needed packages
os.system('sudo apt-get install -y build-essential python-smbus i2c-tools avrdude nmap nginx php-fpm php-zip')
# raspi-config
#os.system('sudo raspi-config nonint do_change_locale en_IS.UTF-8')
os.system('sudo raspi-config nonint do_boot_behaviour B2')
os.system('sudo raspi-config nonint do_camera 0')
os.system('sudo raspi-config nonint do_ssh 0')
os.system('sudo raspi-config nonint do_i2c 0')
os.system('sudo raspi-config nonint do_rgpio 0')
# Add alias list to .bashrc
os.system('sudo cat source/Minion_alias.txt >> /home/pi/.bashrc')
#Create Driver Location
os.system('sudo mkdir /home/pi/Documents/drivers')
# Clone repos
os.chdir('/home/pi/Documents/drivers/')
os.system('git clone https://github.com/bluerobotics/tsys01-python.git')
os.system('git clone https://github.com/bluerobotics/ms5837-python.git')
os.system('git clone https://github.com/bluerobotics/KellerLD-python.git')
os.system('git clone https://github.com/pimoroni/adxl345-python.git')
os.system('git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git')
# Install adc driver
os.chdir('Adafruit_Python_ADS1x15/')
os.system('sudo python setup.py install')

os.system('sudo cp /home/pi/Documents/drivers/adxl345-python/adxl345.py /home/pi/Documents/Minion_scripts/')
os.system('sudo cp /home/pi/Documents/drivers/KellerLD-python/kellerLD.py /home/pi/Documents/Minion_scripts/')
os.system('sudo cp /home/pi/Documents/drivers/ms5837-python/ms5837/ms5837.py /home/pi/Documents/Minion_scripts/')
os.system('sudo cp -r /home/pi/Documents/drivers/tsys01-python/tsys01 /home/pi/Documents/Minion_scripts/')
# Exit
os.chdir(ini_dir)

# Set up and sync RTC
print("Appending /boot/config.txt")
os.system("echo 'dtoverlay=dwc2' >> /boot/config.txt")
os.system("echo 'dtoverlay=i2c-rtc,ds3231' >> /boot/config.txt")
os.system("echo 'dtoverlay=sc16is752-i2c,int_pin=16,addr=0x49' >> /boot/config.txt")
os.system("echo 'dtoverlay=i2c_baudrate=400000' >> /boot/config.txt")
os.system("echo 'enable_uart=1' >> /boot/config.txt")

print("Appending to /boot/cmdline.txt")
os.system("echo 'modules-load=dwc2,g_ether plymoth.ignore-serial-consoles' >> /boot/cmdline.txt")

# Move scripts to local build
os.system('sudo cp source/Keep_Me_Alive.py source/dhcp-configure.py source/dhcp-switch.py source/RTC_Finish.py source/RTC-set.py source/Shutdown.py source/flasher.py source/Iridium_gps.py source/FishTag_data.py /home/pi/Documents/Minion_tools/')

# Set pi to launch rest of script after reboot
os.system("sudo sed -i '/# Print the IP/isudo python /home/pi/Documents/Minion_tools/RTC_Finish.py\n\n' /etc/rc.local")

os.system("sudo chmod +x /etc/rc.local")

# Set up website
os.system('sudo /etc/init.d/nginx start')

os.system('sudo cp source/web_iface/sites-enabled/default /etc/nginx/sites-enabled/')

os.system('sudo /etc/init.d/nginx reload')

os.system('sudo cp source/web_iface/* /var/www/html/')

os.system('sudo rm -r /var/www/html/index.nginx-debian.html')

webdir = '/var/www/html/'
for filename in os.listdir(webdir):

    if filename.endswith(".php") or filename.endswith(".py") or filename.endswith(".html"):
        webfile = os.path.join(webdir, filename)
        # Add IP address to web files
        with open(webfile, 'r') as file :
            web_conf = file.read()

        # Replace the values
        web_conf = web_conf.replace('XXX', '{}'.format(IP_addr))

        # Write the file out again
        with open(webfile, 'w') as file:
            file.write(web_conf)
    else:
        continue

os.system('sudo chown -R www-data /var/www/html/')

os.system('sudo chmod +x /var/www/html/*')

os.system('sudo sed -i "$ a www-data ALL=(ALL) NOPASSWD:ALL" /etc/sudoers')

os.system('sudo cp source/web_iface/php.ini /etc/php/7.3/cli/')

# Reboot to finish kernel module config
os.system('sudo shutdown now')
