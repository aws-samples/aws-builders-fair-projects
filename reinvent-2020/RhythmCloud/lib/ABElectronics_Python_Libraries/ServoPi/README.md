AB Electronics UK Servo Pi Python Library
=====

Python Library to use with Servo Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/ServoPi/demos  

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

The Servo Pi library is located in the ServoPi directory

The library requires smbus2 or python-smbus to be installed.  

For Python 2.7:
```
sudo pip install smbus2
```
For Python 3.5:
```
sudo pip3 install smbus2
```

# Class: PWM #

The PWM class provides control over the pulse-width modution outputs on the PCA9685 controller.  Functions include setting the frequency and duty cycle for each channel.  

Initialise with the I2C address for the Servo Pi.

```
pwmobject = PWM(0x40)
```

Functions:
----------

```
set_pwm_freq(freq, calibration) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency, calibration - optional integer value to offset oscillator errors.  
**Returns:** null  

```
set_pwm(channel, on, off) 
```
Set the output on single channels  
**Parameters:** channel - 1 to 16, on - time period 0 to 4095 , off - time period 0 to 4095.  Total on time and off time can not exceed 4095  
**Returns:** null  

```
set_pwm_on_time(channel, on_time) 
```
Set the output on time for a single channels  
**Parameters:** channel - 1 to 16, on - time period 0 to 4095  
**Returns:** null  

```
set_pwm_off_time(self, channel, off_time) 
```
Set the output off time for a single channels  
**Parameters:** channel - 1 to 16, off_time - time period 0 to 4095  
**Returns:** null  

```
get_pwm_on_time(channel) 
```
Get the output on time for a single channels  
**Parameters:** channel - 1 to 16  
**Returns:** on time - integer 0 to 4095  

```
get_pwm_off_time(channel) 
```
Get the output off time for a single channels  
**Parameters:** channel - 1 to 16  
**Returns:** on time - integer 0 to 4095  


```
set_all_pwm(on, off) 
```
Set the output on all channels  
**Parameters:** on - time period, off - time period 0 to 4095.  Total on time and off time can not exceed 4095  
**Returns:** null  

```
output_disable()
```
Disable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
output_enable()
```
Enable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
set_allcall_address(address)
```
Set the I2C address for the All Call function  
**Parameters:** address  
**Returns:** null  

```
enable_allcall_address()
```
Enable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```
disable_allcall_address()
```
Disable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```
sleep()
```
Puts the PCA9685 PWM controller into a sleep state.  
**Parameters:** null  
**Returns:** null  

```
wake()
```
Wakes the PCA9685 PWM controller from its sleep state.  
**Parameters:** null  
**Returns:** null  

```
is_sleeping()
```
Returns if the PCA9685 PWM controller is in its sleep state.  
**Parameters:** null  
**Returns:** True = Is sleeping, False = Is awake.  

```
invert_output(state)
```
Inverts the outputs on all PWM channels.  
**Parameters:** True = inverted, False = non-inverted  
**Returns:** null  

# Class: Servo #

The Servo class provides functions for controlling the position of servo motors commonly used on radio control models and small robots.  The Servo class initialises with a default frequency of 50Hz and low and high limits of 1ms and 2ms.

Initialise with the I2C address for the Servo Pi.

```
servo_object = Servo(0x40)
```
**Optional Parameters:**  
low_limit = Pulse length in milliseconds for the lower servo limit. (default = 1.0ms)  
high_limit = Pulse length in milliseconds for the upper servo limit. (default = 2.0ms)  
reset = True: reset the servo controller and turn off all channels .  False: initialise with existing servo positions and frequency. (default = true)  

Functions:
----------

```
move(channel, position, steps=250) 
```
Set the servo position  
**Parameters:**  
channel - 1 to 16  
position - value between 0 and the maximum number of steps.  
steps (optional) - The number of steps between the the low and high servo limits.  This is preset at 250 but can be any number between 0 and 4095.  On a typical RC servo a step value of 250 is recommended.  
**Returns:** null  

```
get_position(channel, steps=250) 
```
Get the servo position  
**Parameters:** 
channel - 1 to 16  
steps (optional) - The number of steps between the the low and high servo limits.  This is preset at 250 but can be any number between 0 and 4095.  On a typical RC servo a step value of 250 is recommended.  
**Returns:** position - value between 0 and the maximum number of steps. Due to rounding errors when calculating the position, the returned value may not be exactly the same as the set value. 

```
set_low_limit(low_limit, channel)
```
Set the pulse length for the lower servo limits.  Typically around 1ms.  
Warning: Setting the pulse limit below 1ms may damage your servo.  
**Parameters:**  
low_limit - Pulse length in milliseconds for the lower servo limit.  
channel (optional) - The channel for which the low limit will be set.  
If this value is omitted the low limit will be set for all channels.  
**Returns:** null  

```
set_high_limit(high_limit, channel)
```
Set the pulse length for the upper servo limits.  Typically around 2ms. 
Warning: Setting the pulse limit above 2ms may damage your servo.  
**Parameters:**  
high_limit - Pulse length in milliseconds for the upper servo limit.  
channel (optional) - The channel for which the low limit will be set.  
If this value is omitted the low limit will be set for all channels.  
**Returns:** null  

```
set_frequency(freq, calibration) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency for the servo.  
calibration - optional integer value to offset oscillator errors.  
**Returns:** null  

```
output_disable()
```
Disable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
output_enable()
```
Enable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
sleep()
```
Puts the PCA9685 PWM controller into a sleep state.  
**Parameters:** null  
**Returns:** null  

```
wake()
```
Wakes the PCA9685 PWM controller from its sleep state.  
**Parameters:** null  
**Returns:** null  

```
is_sleeping()
```
Returns if the PCA9685 PWM controller is in its sleep state.  
**Parameters:** null  
**Returns:** True = Is sleeping, False = Is awake.  

Usage
====

**PWM Class**

To use the Servo Pi PWM class in your code you must first import the class:
```
from ServoPi import PWM
```
Next you must initialise the PWM object:
```
pwm = PWM(0x40)
```
Set PWM frequency to 200 Hz and enable the output
```
pwm.set_pwm_freq(200)  
pwm.output_enable()  
```
Set the pulse with of channel 1 to 1024 or 25% duty cycle
```
pwm.set_pwm(1, 0, 1024) 
```

**Servo Class**

To use the Servo Pi Servo class in your code you must first import the class:
```
from ServoPi import Servo
```
Next you must initialise the Servo object:
```
servo = Servo(0x40)
```
Set PWM frequency to 50 Hz
```
servo.set_frequency(50)  
```
Move the servo on channel 1 to position 125 out of 250 steps  
```
servo.move(1, 125, 250)
```

