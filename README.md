# rpimcp4822
### Author: 
Mike Willems
### Last Revision:
2018.05.17
### Overview: 
This class extends spidev for working with the Microchip MCP4822 DAC specifically with a Raspberry Pi model 3B using the spidev library. It may work with other versions, but please double check the BroadCom (BCM) pin numbering before using.
### Functions List:
 - constructor(bus_num=0, device_num=0, open=True, max_speed_khz=20000, output_latch_pin=-1)
 - ready(bus_num=0, device_num=0)
 - write(mV, spidev_obj, channel, not_GA=0)
 - shutdown(spidev_obj, channel=2)
 - setup_latch(pin_num=25, mode=GPIO.BCM)
 - update_output(pulse_width=0.0000002, constant=False)
 - cleanup()
## Function Descriptions
### CONSTRUCTOR

Returns an object for accessing a particular BCM4822 chip. Opens device 0 on bus 0 by default at 20MHz.

#### Parameters:
##### bus_num (optional)
    0 default, the only one available on the GPIO header of the RPi (BCM pins 7-11, physical pins 19,
    21, 23, 24, 26)

##### device_num (optional)
    0 default, can be 1 or 2 while using the RPi GPIO header
    
##### open (optional)
    True by default, clear to keep the SPI GPIO pins off and open later on demand, e.g. for power
    saving.
    
##### max_speed_khz (optional)
    20000 (20MHz) by default, the max rated clock speed of the MCP4822 is 20MHz. Max clock speed of the
    Raspberry Pi 3B SPI controller is 125MHz, though only certain values are supported: the RPi rounds
    down to the closest supported value, in the max case, 15.6MHz. See this page for more info:
    https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
    NOTE: be careful if using header wires - most can't support more than ~5MHz, so try setting this
    lower (maybe 100) if you experience trouble getting the chip to work.
    
##### output_latch_pin (optional)
    -1 by default to indicate not used. This is the (BCM) number of the output latch pin. If included
    in the constructor, then the output_latch_pin gets set up. If BOARD numbering is desired, this
    variable must be set using the setup_output_latch() function.


Note that spidev's mode functionality works fine, and it works fine by default with the MCP4822, so I haven't
wrapped it. It can be accessed directly with spidev if desired, since this class inherits all spidev
functions. If using, either 0,0 or 1,1 work according to the datasheet.


### WRITE

Writes a particular voltage to the MCP4822 over SPI using the spidev library.

#### Parameters:
##### mV
    Voltage to write in mV. If using the chip in 1x voltage mode (not-GA pin high for Vref x 1 = 2.048V max),
    then this should be a float multiple of 0.5 between 0 and 2047.5 inclusive, else an integer between 0 and
    4096 (2^12) inclusive. Alternatively, you can pass in a hex value, but make sure that in that case, not_GA
    is left as 0.
     
##### spidev_obj
    The spidev object on which to write. Must have an opened bus / device.

##### channel
    0 = channel A
    1 = channel B

##### not_GA (optional)
    0 by default, set this parameter to use the 4822 in single-gain mode (Vref x 1 = 2.048V max with 0.5mV
    steps)

#### Operation:
The input is multiplied by two if in not_GA mode, split as a 12-bit hex value into the least significant byte
and the most significant nibble. The appropriate configuration bits are then prepended to the input.

Note that this command effectively handles the not_CS, SCK, and MOSI (SDI) signals, using the output latching,
not_LDAC, is handled separately via the update_output function. By default, not_LDAC is held low and input is
immediately (in one additional clock cycle) transferred from the input register to the DAC register.


### SHUTDOWN

Sends a shutdown signal to the MCP4822.

#### Parameters:
##### spidev_obj
    A spidev object for communicating with the spi device to be shut down.

##### channel (optional)
    Selects the channel (A = 0 or B = 1) to shut down with output = 0V. 2 (default) shuts down both.
    

### SETUP_OUTPUT_LATCH

Uses RPi.GPIO to configure GPIO pin for controlling not_LDAC on the MCP4822.

#### Parameters:
##### pin_num (optional)
    BCM pin 25 (GPIO25, physical pin 22) by default because of proximity to other SPI pins.

##### mode (optional)
    GPIO.BCM for BroadCom numbering by default. To access pins besides the BCM designated pins, set mode to
    GPIO.BOARD.


### UPDATE_OUTPUT

Pulses the output_latch_pin (for connection to the not_LDAC pin) voltage low to trigger updating the DAC /
output registers to match the input register. If the constant parameter is set, then turns off latched
output functionality.

#### Parameters:
##### pulse_width (optional)
    0.0000002 by default, the minimal reasonable value. The MCP4822's min time for an LDAC pulse is 100ns,
    but the Pi can't realistically do that. Default is 200ns, and will probably manifest closer to 1-10us. Set constant to turn off latching and update on set.

    
##### constant (optional)
    False by default, True will keep the not_LDAC pin low to remain in synchronous output mode.


### CLEANUP

Closes the spidev object and calls the GPIO cleanup function.
