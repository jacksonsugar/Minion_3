AVRdude argument for programming fuses

    avrdude -c usbtiny -p atmega328p -U lfuse:w:0xe2:m -U hfuse:w:0xd9:m -U efuse:w:0xff:m

Dependencies and code for programming the HAT microcontroller

Install avrdude:

apt (Debian):

    sudo apt-get install avrdude

homebrew (OSX):

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

    brew install avrdude

Windows:

    https://www.ladyada.net/learn/avr/setup-win.html

Steps for deployment

1) Download and install Arduino IDE from the official website:  https://www.arduino.cc/en/Main/Software
2) Clone this repository to your device by following the green link above [Download ZIP]
3) Open Adruino IDE and configure bootloader for the ATmega328p and USBtiny programmer

      Tools -> Board: -> Arduino Pro or Pro Mini (3.3V, 8MHz) w/ Atmega328

      Tools -> Programmer -> USBtinyISP

4) Import .zip libraries from repository into Arduino IDE 

      Sketch -> Include Library -> Add .ZIP Library..
            
            LowPower.zip

5) Connect the HAT and programmer to your laptop and open terminal

       sudo avrdude -c usbtiny -p atmega328p -v
      
      This checks the state of the microcontroller 
      
      If fuses do not return (E:FF, L:E2, H:D9)
      
       sudo avrdude -c usbtiny -p atmega328p -F -U lfuse:w:0xe2:m -U hfuse:w:0xd9:m -U efuse:w:0xff:m
 

6) Open Minion_2.9_uC.ino and set the sleep interval

7) Upload software to HAT

      File --> Upload Using Programmer
      
8) Wait for flash to verify upload

9) Unplug Programmer

