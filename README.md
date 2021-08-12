# Minion 3 Install Instructions

### Prepare a fresh install of raspbian on micro-sd card:

https://www.raspberrypi.org/software/

I highly recomend the raspberry pi foundation's rpi-imager

### Power Pi via micro-USB

At this stage you should have:

- SD card in Pi
- Wired LAN
- Keyboard/Mouse
- Monitor
- No HAT

### Follow on screen instructions

Install raspbian as normal

Choose any password for the device

Skip wireless setup

When prompted, update the computer

Allow it to reboot

### Clone Repo and Install

Once the Pi reboots, open a terminal and type this command to download the repo:


  `~$ sudo git clone https://github.com/jacksonsugar/Minion_3.git`
  
Now navigate into the folder and begin the install process:
  
  `~$ cd Minion_3/`
  
  `~/Minion/$ sudo python Minion_install.py`
  
  
  
  
  
  
  
  
  
  
  
