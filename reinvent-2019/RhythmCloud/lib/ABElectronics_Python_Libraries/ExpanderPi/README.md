AB Electronics UK Expander Pi Python Library
=====

Python Library to use with Expander Pi board from https://www.abelectronics.co.uk

The Expander Pi contains separate classes for the real-time clock, analogue to digital converter, digital to analogue converter and the digital I/O pins.  Examples are included to show how each of the classes can be used.

The example python files can be found in /ABElectronics_Python_Libraries/ExpanderPi/demos  

### Downloading and Installing the library

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library navigate into the ABElectronics_Python_Libraries folder and run:  

For Python 2.7:
```
sudo python setup.py install
```
For Python 3.5:
```
sudo python3 setup.py install
```

If you have PIP installed you can install the library directly from github with the following command:

For Python 2.7:
```
sudo python2.7 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

For Python 3.5:
```
sudo python3.4 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The Expander Pi library is located in the ExpanderPi directory

The library requires smbus2 or python-smbus to be installed.  

For Python 2.7:
```
sudo pip install smbus2
```
For Python 3.5:
```
sudo pip3 install smbus2
```

# Class: ADC #

The ADC class controls the functions on the 12 bit 8 channel Analogue to Digital converter.  The Expander Pi comes with an on board  4.096 voltage reference.  To use an external voltage reference remover the solder bridge from jumper J1 and connect the external voltage reference to the Vref pin.

Functions:
----------


```
read_adc_voltage(channel, mode) 
```   
Read the voltage from the selected channel on the ADC   
**Parameters:** channel = options are: 1 to 8 , mode = 0 or 1 - 0 = single ended, 1 = differential
**Returns:** voltage

In single ended mode the channel number corresponds to the number on the Expander Pi.  In differential mode channel the number selects the channels as follows:

| Channel  | Mode         | Channel Selection On Expander Pi   |
|-------|--------------|----------------------|
| 1     | single-ended | 1                    |
| 2     | single-ended | 2                    |
| 3     | single-ended | 3                    |
| 4     | single-ended | 4                    |
| 5     | single-ended | 5                    |
| 6     | single-ended | 6                    |
| 7     | single-ended | 7                    |
| 8     | single-ended | 8                    |
| 1     | differential | CH1 = IN+  CH2 = IN- |
| 2     | differential | CH1 = IN-  CH2 = IN+ |
| 3     | differential | CH3 = IN+  CH4 = IN- |
| 4     | differential | CH3 = IN-  CH4 = IN+ |
| 5     | differential | CH5 = IN+  CH6 = IN- |
| 6     | differential | CH5 = IN-  CH6 = IN+ |
| 7     | differential | CH7 = IN+  CH8 = IN- |
| 8     | differential | CH7 = IN-  CH8 = IN+ |


```
read_adc_raw(channel, mode) 
```   
Read the raw value from the selected channel on the ADC   
**Parameters:** channel = options are: 1 to 8 , mode = 0 or 1 - 0 = single ended, 1 = differential  
**Returns:** raw 12 bit value (0 to 4096)

In single ended mode the channel number corresponds to the number on the Expander Pi.  In differential mode channel the number selects the channels as follows:

| Channel  | Mode         | Channel Selection On Expander Pi   |
|-------|--------------|----------------------|
| 1     | single-ended | 1                    |
| 2     | single-ended | 2                    |
| 3     | single-ended | 3                    |
| 4     | single-ended | 4                    |
| 5     | single-ended | 5                    |
| 6     | single-ended | 6                    |
| 7     | single-ended | 7                    |
| 8     | single-ended | 8                    |
| 1     | differential | CH1 = IN+  CH2 = IN- |
| 2     | differential | CH1 = IN-  CH2 = IN+ |
| 3     | differential | CH3 = IN+  CH4 = IN- |
| 4     | differential | CH3 = IN-  CH4 = IN+ |
| 5     | differential | CH5 = IN+  CH6 = IN- |
| 6     | differential | CH5 = IN-  CH6 = IN+ |
| 7     | differential | CH7 = IN+  CH8 = IN- |
| 8     | differential | CH7 = IN-  CH8 = IN+ |



```
set_adc_refvoltage(voltage) 
```   
set the reference voltage for the analogue to digital converter.  
By default the ADC uses an on-board 4.096V voltage reference.  If you choose to use an external voltage reference you will need to use this method to set the ADC reference voltage to match the supplied reference voltage.
The reference voltage must be less than or equal to the voltage on the Raspberry Pi 5V rail. 

**Parameters:** voltage (use a decimal number)   
**Returns:** null



Usage
====

To use the ADC class in your code you must first import the library:

```
from ExpanderPi import ADC
```

Next you must initialise the ADC object:

```
adc = ADC()
```

If you are using an external voltage reference set the voltage using:

```
adc.set_adc_refvoltage(4.096)
```

Read the voltage from the ADC channel 1 in single ended mode at 1 second intervals:

```
while (True):
  print adc.read_adc_voltage(1,0)
  time.sleep(1)
```

# Class: DAC #

The DAC class controls the 2 channel 12 bit digital to analogue converter.  The DAC uses an internal voltage reference and can output a voltage between 0 and 2.048V.
A gain setting allows you to increase the voltage to between 0 and 4.095V when gain is set to 2

Functions:
----------

```
set_dac_voltage(channel, voltage)
```

Set the voltage for the selected channel on the DAC  
**Parameters:** channel - 1 or 2,  voltage can be between 0 and 2.047 volts when gain is set to 1 or 0 and 4.095 volts when gain is set to 2
**Returns:** null 

```
set_dac_raw(channel, value)
```

Set the raw value from the selected channel on the DAC  
**Parameters:** channel - 1 or 2,value int between 0 and 4095  
**Returns:** null 

Usage
====

To use the DAC class in your code you must first import the library:

```
from ExpanderPi import DAC
```

Next you must initialise the DAC object with a gain setting of 1 or 2:

```
dac = DAC(1)
```

Set the channel and voltage for the DAC output.

```
dac.set_dac_voltage(1, 1.5)
```

# Class: IO #

The IO class controls the 16 digital I/O channels on the Expander Pi.  The MCP23017 chip is split into two 8-bit ports.  Port 0 controls pins 1 to 8 while Port 1 controls pins 9 to 16. 
When writing to or reading from a port the least significant bit represents the lowest numbered pin on the selected port.

Functions:
----------

```
set_pin_direction(pin, direction):
```

Sets the IO direction for an individual pin  
**Parameters:** pin - 1 to 16, direction - 1 = input, 0 = output  
**Returns:** null

```
set_port_direction(port, direction): 
```

Sets the IO direction for the specified IO port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, direction - byte value between 0 and 255, each bit of the byte represents one pin. 1 = input, 0 = output  
**Returns:** null

```
get_port_direction(port): 
```

Gets the IO direction for the specified IO port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16 
**Returns:** value between 0 and 255

```
set_pin_pullup(pin, value)
```

Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:** pin - 1 to 16, value: 1 = Enabled, 0 = Disabled  
**Returns:** null

```
set_port_pullups(port, value)
```

Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:** port - 0 or 1, value: 0 to 255  
**Returns:** null

```
get_port_pullups(port)
```

Get the value of the internal 100K pull-up resistors for the selected IO port  
**Parameters:** port - 1 to 16
**Returns:** null

```
write_pin(pin, value)
```

Write to an individual pin 1 - 16  
**Parameters:** pin - 1 to 16, value - 1 = Enabled, 0 = Disabled
**Returns:** null

```
write_port(port, value)
```

Write to all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, value -  number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
read_pin(pin)
```

Read the value of an individual pin 1 - 16   
**Parameters:** pin: 1 to 16  
**Returns:** 0 = logic level low, 1 = logic level high

```
read_port(port)
```

Read all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF

```
invert_port(port, polarity)
```

Invert the polarity of the pins on a selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, polarity - byte value between 0 and 255, each bit of the byte represents one pin. 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null

```
get_port_polarity(port)
```

Get the polarity for the selected IO port
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16 
**Returns:** byte value between 0 and 255, each bit of the byte represents one pin. 0 = same logic state of the input pin, 1 = inverted logic state of the input pin 

```
invert_pin(pin, polarity)
```

Invert the polarity of the selected pin  
**Parameters:** pin - 1 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
**Returns:** null

```
mirror_interrupts(value)
```

Mirror Interrupts  
**Parameters:** value - 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INTA is associated with PortA and INTB is associated with PortB  
**Returns:** null

```
set_interrupt_type(port, value)
```

Sets the type of interrupt for each pin on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: 1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change  
**Returns:** null

```
set_interrupt_polarity(value)
```
Sets the polarity of the INT output pins  
**Parameters:**  
value: 0 = Active Low, 1 = Active High  
**Returns:** null

```
set_interrupt_defaults(port, value)
```

These bits set the compare value for pins configured for interrupt-on-change on the selected port.  
If the associated pin level is the opposite from the register bit, an interrupt occurs.    
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: compare value  
**Returns:** null

```
set_interrupt_on_port(port, value)
```

Enable interrupts for the pins on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
set_interrupt_on_pin(pin, value)
```

Enable interrupts for the selected pin  
**Parameters:** pin - 1 to 16, value - 0 = interrupt disabled, 1 = interrupt enabled  
**Returns:** null

```
read_interrupt_status(port)
```

Enable interrupts for the selected pin  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** status

```
read_interrupt_capture(port)
```

Read the value from the selected port at the time of the last interrupt trigger  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** status

```
reset_interrupts()
```

Set the interrupts A and B to 0  
**Parameters:** null  
**Returns:** null

Usage
====

To use the IO Pi library in your code you must first import the library:

```
from ExpanderPi import IO
```

Next you must initialise the IO object:

```
io = IO()
```

By default the IO object will be initialised in a reset state with the ports set as inputs, pull-up resistors disabled and the pins non-inverted.  If you want to initialase the IO object without updating the port direction or the pull-up status you can add a reset=False parameter.

```
io = IO(reset=False)
```

We will read the inputs 1 to 8 from the I/O bus so set port 0 to be inputs and enable the internal pull-up resistors 

```
io.set_port_direction(0, 0xFF)
io.set_port_pullups(0, 0xFF)
```

You can now read the pin 1 with:
```
print 'Pin 1: ' + str(io.read_pin(1))
```

# Class: RTC #

The RTC class controls the DS1307 real-time clock on the Expander Pi.  You can set and read the date and time from the clock as well as controlling the pulse output on the RTC pin.

Functions:
----------

```
set_date(date) 
```

Set the date and time on the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Parameters:** date   
**Returns:** null

```
read_date() 
```

Returns the date from the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Returns:** date


```
enable_output() 
```

Enable the square-wave output on the SQW pin.  
**Returns:** null

```
disable_output()
```

Disable the square-wave output on the SQW pin.   
**Returns:** null

```
set_frequency(frequency)
```

Set the frequency for the square-wave output on the SQW pin.   
**Parameters:** frequency - options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz   
**Returns:** null

```
write_memory(address, valuearray)
```
Write to the memory on the ds1307. The ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes  
**Parameters:** address - 0x08 to 0x3F  
valuearray - byte array containing data to be written to memory  
**Returns:** null

```
read_memory(address, length)
```
Read from the memory on the ds1307  
**Parameters:** address - 0x08 to 0x3F 
length - up to 32 bytes.  
length can not exceed the available address space.  
**Returns:** array of bytes

Usage
====

To use the RTC class in your code you must first import the library:

```
from ExpanderPi import RTC
```

Next you must initialise the RTC object:

```
rtc = RTC()
```

Set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS :

```
rtc.set_date("2013-04-23T12:32:11")
```

Enable the square-wave output at 8.192KHz on the SQW pin:

```
rtc.set_frequency(3)
rtc.enable_output()
```

Read the current date and time from the RTC at 1 second intervals:

```
while (True):
  print rtc.read_date()
  time.sleep(1)
```
