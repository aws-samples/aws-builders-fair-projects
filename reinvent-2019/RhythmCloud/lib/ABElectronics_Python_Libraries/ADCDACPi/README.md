AB Electronics UK ADCDAC Pi Python Library
=====

Python Library to use with ADCDAC Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/ADCDACPi/demos.

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
sudo python3.5 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```


Functions:
----------

Initialising the ADCDACPi object.  
```
adcdac = ADCDACPi(gain_factor)
```
**Parameter:** gain_factor - 1 or 2
When the gain is set to 1 the voltage range of the DAC will be 0 to 2.048V.  When gain is set to 2 the voltage will be 0 to 3.3V  

```
read_adc_voltage(channel, mode) 
```
Read the voltage from the selected channel on the ADC  
**Parameter:** channel - 1 or 2  
**Parameter:** mode - 0 = single ended, 1 = differential  
**Returns:** number as float between 0 and 2.048

```
read_adc_raw(channel, mode) 
```
Read the raw value from the selected channel on the ADC  
**Parameter:** channel - 1 or 2  
**Parameter:** mode - 0 = single ended, 1 = differential  
**Returns:** int  
```
set_adc_refvoltage(voltage)
```
Set the reference voltage for the analogue to digital converter.  
The ADC uses the raspberry pi 3.3V power as a voltage reference so using this method to set the reference to match the exact output voltage from the 3.3V regulator will increase the accuracy of the ADC readings.  
**Parameters:** voltage  
**Returns:** null  

```
set_dac_voltage(channel, voltage)
```
Set the voltage for the selected channel on the DAC.  The DAC has two gain values, 1 or 2, which can be set when the ADCDAC object is created.  A gain of 1 will give a voltage between 0 and 2.047 volts.  A gain of 2 will give a voltage between 0 and 3.3 volts.  
**Parameters:** channel - 1 or 2,  voltage can be between 0 and 2.047 volts  
**Returns:** null 

```
set_dac_raw(channel, value)
```
Set the raw value from the selected channel on the DAC  
**Parameters:** channel - 1 or 2,value int between 0 and 4095  
**Returns:** null 

Usage
====

To use the ADCDAC Pi library in your code you must first import the library:
```
from ADCDACPi import ADCDACPi
```
Next you must initialise the adcdac object and set a gain of 1 or 2 for the DAC:
```
adcdac = ADCDACPi(1)
```
Set the reference voltage.
```
adcdac.set_adc_refvoltage(3.3)
```
Read the voltage from channel 2 and display on the screen
```
print adcdac.read_adc_voltage(2)
```
