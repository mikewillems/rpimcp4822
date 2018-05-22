'''
rpimcp4822.py
Author: Mike Willems
Last Revision: 2018.05.21
Description: This class extends spidev for working with the Microchip MCP4822 DAC specifically with
a Raspberry Pi model 3B using the spidev library. It may work with other versions, but please double
check the BroadCom (BCM) pin numbering before using.
License: MIT - Code comes with no warranty or disclaimer and may be used or modified freely for whatever
purpose, personal or commercial, so long as this attribution and license is included. 
'''

import spidev
import RPi.GPIO as GPIO
import time

class RPiMCP4822(spidev.SpiDev):
    def __init__(self, bus_num=0, device_num=0, open=True, max_speed_khz=20000, output_latch_pin=-1):
        self.bus_num = bus_num
        self.device_num = device_num
        if (open):
            self.open(bus_num, device_num) # on the RPi, sets the CS pin (BCM24 for 0, 26 for 1).
            self.max_speed_hz = max_speed_khz * 1000
        self.max_speed_khz = max_speed_khz
        self.output_latch_pin = output_latch_pin
        if (output_latch_pin > 0):
            setup_output_latch(output_latch_pin)


    def ready(self, bus_num=0, device_num=0, max_speed_khz=20000):
        self.open(bus_num, device_num)
        self.max_speed_hz = max_speed_khz * 1000


    def write(self, mV, channel, not_GA=False):
        lsB = mV & 0xFF # bit screen to select only the 8 least significant bits of mV
        msB = (
            mV >> 8
            | 0x10 # not_SHDN bit
            | 0x20 * not_GA # not_GA bit
            | 0x80 * channel # channel bit: & with 1 to select only least significant bit = 0/1 for 0xA/B
            )
        self.xfer([msB, lsB])


    def shutdown(self, channel=2):
        if(channel ^ 1): # if channel A should be shutdown (0 or 2)
            self.xfer([0,0])
        if (channel | channel >> 1): # if channel B should be shutdown (1 or 2)
            self.xfer([0x80,0])


    def setup_output_latch(self, pin_num=25, mode=GPIO.BCM):
        self.output_latch_pin = pin_num
        GPIO.setmode(mode)
        GPIO.setup(pin_num, GPIO.OUT)
        GPIO.output(pin_num, GPIO.HIGH)
	    
	    
    def update_output(self, pulse_width=0.0000002, constant=False):
        GPIO.output(self.output_latch_pin, GPIO.LOW)
        time.sleep(pulse_width)
        if(not constant):
            GPIO.output(self.output_latch_pin, GPIO.HIGH)


    def cleanup():
        self.close()
        if(self.output_latch_pin > -1):
            GPIO.output(self.output_latch_pin, GPIO.LOW)
            GPIO.cleanup()
