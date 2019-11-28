AB Electronics Python Libraries
=====

Python Libraries to work with Raspberry Pi expansion boards from https://www.abelectronics.co.uk

#### 07-07-2017 Major Update - Now compatible with Python 2 and 3

Version 2.0.0 of the Python library has introduced several changes to the structure of the classes and demo files.  The major changes are listed below.  Please read CHANGELOG.md for a complete list of changes.

* Files renamed: removed ABE_ from all names.  
ABE_ADCDACPi > ADCDACPi  
ABE_ADCDifferentialPi > ADCDifferentialPi  
ABE_ADCPi > ADCPi  
ABE_ExpanderPi > ExpanderPi  
ABE_IOPi > IOPi  
ABE_RTCPi > RTCPi  
ABE_ServoPi >  ServoPi

* All classes and demo files are now compatible with Python 2 and 3.  The ABElectronics_Python3_Libraries will no longer be updated so please use this version instead for your Python 3 projects.
* Moved all demo files into demo sub-folders for each class
* The ABE_Helper class has been integrated into the board classes and does not need to be imported separately.
* Added a setup.py into the root for installing the this library into the main Python library directory.

Previous versions of the Python libraries can be found at https://github.com/abelectronicsuk/Archive

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

### ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the ADC DAC Pi  
https://www.abelectronics.co.uk/p/39/ADC-DAC-Pi-Raspberry-Pi-ADC-and-DAC-expansion-board and the ADC DAC Pi Zero  
https://www.abelectronics.co.uk/p/74/ADC-DAC-Pi-Zero-Raspberry-Pi-ADC-and-DAC-expansion-board
### ADCPi 
This directory contains ADC Pi Python Library  and read voltage demo to use with the ADC Pi   
https://www.abelectronics.co.uk/p/69/ADC-Pi-Raspberry-Pi-Analogue-to-Digital-converter
### ADCDifferentialPi 
This directory contains ADC Differential Pi Python Library and read voltage demo to use with the ADC Differential Pi.  
https://www.abelectronics.co.uk/p/65/ADC-Differential-Pi-Raspberry-Pi-Analogue-to-Digital-converter  
This library is also compatible with the Delta-Sigma Pi.  
https://www.abelectronics.co.uk/kb/article/1041/delta-sigma-pi
### ExpanderPi
This directory contains IO Pi Python Library  and demos to use with the Expander Pi https://www.abelectronics.co.uk/kb/article/1046/expander-pi
### IOPi
This directory contains IO Pi Python Library  and demos to use with the IO Pi Plus https://www.abelectronics.co.uk/p/54/IO-Pi-Plus and IO Pi Zero https://www.abelectronics.co.uk/p/71/IO-Pi-Zero
### RTCPi
This directory contains RTC Pi Python Library and demos to use with the RTC Pi https://www.abelectronics.co.uk/p/15/RTC-Pi , RTC Pi Plus https://www.abelectronics.co.uk/p/52/RTC-Pi-Plus and RTC Pi Zero https://www.abelectronics.co.uk/p/70/RTC-Pi-Zero
### ServoPi
This directory contains ServoPi Python Library  and read voltage demo to use with the ServoPi https://www.abelectronics.co.uk/p/44/Servo-PWM-Pi and Servo Pi Zero https://www.abelectronics.co.uk/p/72/Servo-PWM-Pi-Zero
