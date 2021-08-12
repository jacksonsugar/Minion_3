# Minion 3 Install Instructions

### Prepare a fresh install of raspbian on micro-sd card:

https://www.raspberrypi.org/software/

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I highly recomend the raspberry pi foundation's rpi-imager

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
  
  Assign the device with an IP address between 2 and 250
  
  Enter [Y] to enable debug mode
  
  Enter [N] to choose to have files saved to the Desktop
  
  Allow the installer to finish and it will turn the Pi off.
  
  Finally power on the Minion_Hub and Master_Hub
  
  ### Attach HAT and power 12V via the 4 pin JST
  
  The Pi will boot up and complete it's installation (setting the clock)
  
  Then the Pi will reboot
  
  Once the Pi reboots you may disconnect the LAN network cable
  
  ### Test if the Minion is working
  
  Connect to the Minion_Hub with your cell phone or another computer:
  
  Open a brouser and type the IP of the Minion
  
  (i.e. 192.168.0.XXX)
  
  If you are greeted with a website then you did it!
  
  
  
  
  
