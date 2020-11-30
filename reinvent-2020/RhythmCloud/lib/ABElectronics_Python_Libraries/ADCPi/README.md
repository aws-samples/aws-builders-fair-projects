AB Electronics UK ADC Pi Python Library
=====

Python Library to use with ADC Pi Raspberry Pi expansion board from  
https://www.abelectronics.co.uk  

The example python files can be found in /ABElectronics_Python_Libraries/ADCPi/demos  

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

The ADC Pi library is located in the ADCPi directory  

The library requires smbus2 or python-smbus to be installed.  
  
For Python 2.7:
```
sudo pip install smbus2
```
For Python 3.5:
```
sudo pip3 install smbus2
```

Functions:
----------
```
read_voltage(channel) 
```
Read the voltage from the selected channel  
**Parameters:** channel - 1 to 8  
**Returns:** number as float between 0 and 5.0

```
read_raw(channel) 
```
Read the raw int value from the selected channel  
**Parameters:** channel - 1 to 8  
**Returns:** number as int

```
set_pga(gain)
```
Set the gain of the PGA on the chip  
**Parameters:** gain -  1, 2, 4, 8  
**Returns:** null

```
setBitRate(rate)
```
Set the sample bit rate of the adc  
**Parameters:** rate -  12, 14, 16, 18  
**Returns:** null  
12 = 12 bit (240SPS max)  
14 = 14 bit (60SPS max)  
16 = 16 bit (15SPS max)  
18 = 18 bit (3.75SPS max)  

```
set_conversion_mode(mode)
```
Set the conversion mode for the adc  
**Parameters:** mode -  0 = One-shot conversion, 1 = Continuous conversion  
**Returns:** null

Usage
====

To use the ADC Pi library in your code you must first import the library:
```
from ADCPi import ADCPi
```

Next you must initialise the adc object:
```
adc = ADCPi(0x68, 0x69, 18)
```
The first two arguments are the I2C addresses of the ADC chips. The values shown are the default addresses of the ADC board.  

The third argument is the sample bit rate you want to use on the adc chips. Sample rate can be 12, 14, 16 or 18  

You can now read the voltage from channel 1 with:
```
adc.read_voltage(1)
```
