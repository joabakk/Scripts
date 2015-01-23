# This script will wait for a button to be pressed and then shutdown
# the Raspberry Pi.
# The button is to be connected on header 5 between pins 6 and 8.

# http://kampis-elektroecke.de/?page_id=3740
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
# https://pypi.python.org/pypi/RPi.GPIO

import RPi.GPIO as GPIO
import time
import os

# we will use the pin numbering of the SoC, so our pin numbers in the code are 
# the same as the pin numbers on the gpio headers
GPIO.setmode(GPIO.BCM)  

# Pin will be input and will have his pull up resistor activated
# so we only need to connect a button to ground
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #used to identify if hat is on or not...  


# ISR: if our button is pressed, we will have a falling edge on pin 
# this will trigger this interrupt:
def Int_shutdown(channel):  
   # shutdown our Raspberry Pi
   os.system("sudo shutdown -h now")
   #print "good grace"

# Now we are programming pin as an interrupt input
# it will react on a falling edge and call our interrupt routine "Int_shutdown"

if (GPIO.input(20)) == 1:
   #print "hat on board"
   GPIO.add_event_detect(7, GPIO.FALLING, callback = Int_shutdown, bouncetime = 2000)

# do nothing while waiting for button to be pressed
while 1:
        time.sleep(1)


