# Minion 3 Install Instructions

### Prepare a fresh install of raspbian on micro-sd card:

&emsp; https://www.raspberrypi.org/software/

&emsp; I highly recomend the raspberry pi foundation's rpi-imager

### Power Pi via micro-USB

&emsp;At this stage you should have:

- SD card in Pi
- Wired LAN
- Keyboard/Mouse
- Monitor
- No HAT

### Follow on screen instructions

&emsp;Install raspbian as normal

&emsp;Choose any password for the device

&emsp;Skip wireless setup

&emsp;When prompted, update the computer

&emsp;Allow it to reboot

### Clone Repo and Install

&emsp;Once the Pi reboots, open a terminal and type this command to download the repo:


  `~$ sudo git clone https://github.com/jacksonsugar/Minion_3.git`
  
&emsp;Now navigate into the folder and begin the install process:
  
  `~$ cd Minion_3/`
  
  `~/Minion/$ sudo python Minion_install.py`
  
  &emsp;Assign the device with an IP address between 2 and 250
  
  &emsp;Enter [Y] to enable debug mode
  
  &emsp;Enter [N] to choose to have files saved to the Desktop
  
  &emsp;Allow the installer to finish and it will turn the Pi off
  
  &emsp;Disconnect USB power from the Pi
  
  &emsp;Finally power on the Minion_Hub and Master_Hub
  
  ### Attach HAT and power 12V via the 4 pin JST
  
  &emsp;The Pi will boot up and complete it's installation (setting the clock)
  
  &emsp;Then the Pi will reboot
  
  &emsp;Once the Pi reboots you may disconnect the LAN network cable
  
  ### Test if the Minion is working
  
  &emsp;Connect to the Minion_Hub with your cell phone or another computer:
  
  &emsp;Open a brouser and type the IP of the Minion
  
  &emsp;(i.e. 192.168.0.XXX)
  
  &emsp;If you are greeted with a website then you did it!
  
  
  
  
  
