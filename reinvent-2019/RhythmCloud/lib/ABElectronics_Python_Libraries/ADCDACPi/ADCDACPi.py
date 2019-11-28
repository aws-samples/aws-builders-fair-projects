#!/usr/bin/env python
"""
================================================
ABElectronics ADCDAC Pi Analogue to Digital / Digital to Analogue Converter
================================================

Based on the Microchip MCP3202 and MCP4822
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
try:
    import spidev
except ImportError:
    raise ImportError(
        "spidev not found.")


class ADCDACPi:
    """
    Based on the Microchip MCP3202 and MCP4822
    """

    # variables
    __adcrefvoltage = 3.3  # reference voltage for the ADC chip.

    # Define SPI bus and init
    spiADC = spidev.SpiDev()
    spiADC.open(0, 0)
    spiADC.max_speed_hz = (900000)

    spiDAC = spidev.SpiDev()
    spiDAC.open(0, 1)
    spiDAC.max_speed_hz = (20000000)

    dactx = [0, 0]

    # Max DAC output voltage. Depends on gain factor
    # The following table is in the form <gain factor>:<max voltage>

    __dacMaxOutput__ = {
        1: 2.048,  # This is Vref
        2: 3.3  # This is the voltage of the 3.3V rail
    }

    # public methods
    def __init__(self, gain_factor=1):
        """Class Constructor

        gain_factor -- Set the DAC's gain factor. The value should
           be 1 or 2.  Gain factor is used to determine output voltage
           from the formula: Vout = G * Vref * D/4096
           Where G is gain factor, Vref (for this chip) is 2.048 and
           D is the 12-bit digital value
        """
        if (gain_factor != 1) and (gain_factor != 2):
            raise ValueError('DAC __init__: Invalid gain factor. \
                            Must be 1 or 2')
        else:
            self.gain = gain_factor
            self.maxdacvoltage = self.__dacMaxOutput__[self.gain]

    def read_adc_voltage(self, channel, mode):
        """
        Read the voltage from the selected channel on the ADC
         Channel = 1 or 2
        """
        if (channel > 2) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')
        if (mode > 1) or (mode < 0):
            raise ValueError('read_adc_voltage: mode out of range')
        raw = self.read_adc_raw(channel, mode)
        voltage = (self.__adcrefvoltage / 4096) * raw
        return voltage

    def read_adc_raw(self, channel, mode):
        """
        Read the raw value from the selected channel on the ADC
        Channel = 1 or 2
        """
        if (channel > 2) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')
        if (mode > 1) or (mode < 0):
            raise ValueError('read_adc_voltage: mode out of range')
        if mode == 0:
            raw = self.spiADC.xfer2([1, (1 + channel) << 6, 0])
            ret = ((raw[1] & 0x0F) << 8) + (raw[2])
        if mode == 1:
            if channel == 1:
                raw = self.spiADC.xfer2([1, 0x00, 0])
            else:
                raw = self.spiADC.xfer2([1, 0x40, 0])
            ret = ((raw[1]) << 8) + (raw[2])
        return ret

    def set_adc_refvoltage(self, voltage):
        """
        set the reference voltage for the analogue to digital converter.
        The ADC uses the raspberry pi 3.3V power as a voltage reference so
        using this method to set the reference to match the
        exact output voltage from the 3.3V regulator will increase the
        accuracy of the ADC readings.
        """
        if (voltage >= 0.0) and (voltage <= 7.0):
            self.__adcrefvoltage = voltage
        else:
            raise ValueError('set_adc_refvoltage: reference voltage \
                            out of range')
        return

    def set_dac_voltage(self, channel, voltage):
        """
        set the voltage for the selected channel on the DAC
        voltage can be between 0 and 2.047 volts
        """
        if (channel > 2) or (channel < 1):
            raise ValueError('set_dac_voltage: DAC channel needs to be 1 or 2')
        if (voltage >= 0.0) and (voltage < self.maxdacvoltage):
            rawval = (voltage / 2.048) * 4096 / self.gain
            self.set_dac_raw(channel, int(rawval))
        else:
            raise ValueError('set_dac_voltage: voltage out of range')
        return

    def set_dac_raw(self, channel, value):
        """
        Set the raw value from the selected channel on the DAC
        Channel = 1 or 2
        Value between 0 and 4095
        """

        if (channel > 2) or (channel < 1):
            raise ValueError('set_dac_voltage: DAC channel needs to be 1 or 2')
        if (value < 0) and (value > 4095):
            raise ValueError('set_dac_voltage: value out of range')

        self.dactx[1] = (value & 0xff)

        if self.gain == 1:
            self.dactx[0] = (((value >> 8) & 0xff) | (channel - 1) << 7 |
                             1 << 5 | 1 << 4)
        else:
            self.dactx[0] = (((value >> 8) & 0xff) | (channel - 1) << 7 |
                             1 << 4)

        # Write to device
        self.spiDAC.xfer2(self.dactx)
        return
