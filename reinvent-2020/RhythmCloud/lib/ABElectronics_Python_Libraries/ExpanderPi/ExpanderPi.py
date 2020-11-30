#!/usr/bin/env python
"""
================================================
ABElectronics Expander Pi

Requires smbus2 or python smbus to be installed

================================================
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
try:
    import spidev
except ImportError:
    raise ImportError(
        "spidev not found.")
import re
import platform
import datetime


"""
Private Classes
"""


class _ABEHelpers:
    """
    Local Functions used across all Expander Pi classes
    """

    @staticmethod
    def updatebyte(byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """
        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    @staticmethod
    def get_smbus():
        """
        internal method for getting an instance of the i2c bus
        """
        i2c__bus = 1
        # detect the device that is being used
        device = platform.uname()[1]

        if device == "orangepione":  # running on orange pi one
            i2c__bus = 0

        elif device == "orangepiplus":  # running on orange pi plus
            i2c__bus = 0

        elif device == "orangepipcplus":  # running on orange pi pc plus
            i2c__bus = 0

        elif device == "linaro-alip":  # running on Asus Tinker Board
            i2c__bus = 1

        elif device == "raspberrypi":  # running on raspberry pi
            # detect i2C port number and assign to i2c__bus
            for line in open('/proc/cpuinfo').readlines():
                model = re.match('(.*?)\\s*:\\s*(.*)', line)
                if model:
                    (name, value) = (model.group(1), model.group(2))
                    if name == "Revision":
                        if value[-4:] in ('0002', '0003'):
                            i2c__bus = 0
                        else:
                            i2c__bus = 1
                        break
        try:
            return SMBus(i2c__bus)
        except IOError:
            raise 'Could not open the i2c bus'


"""
Public Classes
"""


class ADC:

    """
    Based on the Microchip MCP3208
    """

    # variables
    __adcrefvoltage = 4.096  # reference voltage for the ADC chip.

    __spiADC = None

    def __init__(self):
        # Define SPI bus and init
        self.__spiADC = spidev.SpiDev()
        self.__spiADC.open(0, 0)
        self.__spiADC.max_speed_hz = (1900000)

    # public methods

    def read_adc_voltage(self, channel, mode):
        """
        Read the voltage from the selected channel on the ADC
        Channel = 1 to 8
        Mode = 0 or 1 -  0 = single ended, 1 = differential
        """
        if (mode < 0) or (mode > 1):
            raise ValueError('read_adc_voltage: mode out of range')
        if (channel > 4) and (mode == 1):
            raise ValueError('read_adc_voltage: channel out of range')
        if (channel > 8) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')

        raw = self.read_adc_raw(channel, mode)
        voltage = (self.__adcrefvoltage / 4096) * raw
        return voltage

    def read_adc_raw(self, channel, mode):
        """
        Read the raw value from the selected channel on the ADC
        Channel = 1 to 8
        Mode = 0 or 1 -  0 = single ended, 1 = differential
        """
        if (mode < 0) or (mode > 1):
            raise ValueError('read_adc_voltage: mode out of range')
        if (channel > 4) and (mode == 1):
            raise ValueError('read_adc_voltage: channel out of range when \
            mode = 1')
        if (channel > 8) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')

        channel = channel - 1
        if mode == 0:
            raw = self.__spiADC.xfer2(
                [6 + (channel >> 2), (channel & 3) << 6, 0])
        if mode == 1:
            raw = self.__spiADC.xfer2(
                [4 + (channel >> 2), (channel & 3) << 6, 0])
        ret = ((raw[1] & 0x0F) << 8) + (raw[2])
        return ret

    def set_adc_refvoltage(self, voltage):
        """
        set the reference voltage for the analogue to digital converter.
        By default the ADC uses an onboard 4.096V voltage reference.  If you
        choose to use an external voltage reference you will need to
        use this method to set the ADC reference voltage to match the
        supplied reference voltage.
        The reference voltage must be less than or equal to the voltage on
        the Raspberry Pi 5V rail.
        """

        if (voltage >= 0.0) and (voltage <= 5.5):
            self.__adcrefvoltage = voltage
        else:
            raise ValueError('set_adc_refvoltage: reference voltage \
                            out of range')
        return


class DAC:

    """
    Based on the Microchip MCP4822

    Define SPI bus and init
    """

    __spiDAC = None
    dactx = [0, 0]

    # Max DAC output voltage.  Depends on gain factor
    # The following table is in the form <gain factor>:<max voltage>
    __dacMaxOutput__ = {
        1: 2.048,  # This is Vref
        2: 4.096  # This is double Vref
    }

    maxdacvoltage = 2.048

    # public methods
    def __init__(self, gainFactor=1):
        """Class Constructor

        gainFactor -- Set the DAC's gain factor. The value should
           be 1 or 2.  Gain factor is used to determine output voltage
           from the formula: Vout = G * Vref * D/4096
           Where G is gain factor, Vref (for this chip) is 2.048 and
           D is the 12-bit digital value
        """

        # Define SPI bus and init
        self.__spiDAC = spidev.SpiDev()
        self.__spiDAC.open(0, 1)
        self.__spiDAC.max_speed_hz = (20000000)

        if (gainFactor != 1) and (gainFactor != 2):
            raise ValueError('DAC __init__: Invalid gain factor. \
                            Must be 1 or 2')
        else:
            self.gain = gainFactor

            self.maxdacvoltage = self.__dacMaxOutput__[self.gain]

    def set_dac_voltage(self, channel, voltage):
        """
        set the voltage for the selected channel on the DAC
        voltage can be between 0 and 2.047 volts when gain is set to 1\
         or 4.096 when gain is set to 2
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
        self.__spiDAC.xfer2(self.dactx)
        return


class IO:

    """
    The MCP23017 chip is split into two 8-bit ports.  port 0 controls pins
    1 to 8 while port 1 controls pins 9 to 16.
    When writing to or reading from a port the least significant bit
    represents the lowest numbered pin on the selected port.
    #
    """

    # Define registers values from datasheet
    IODIRA = 0x00  # IO direction A - 1= input 0 = output
    IODIRB = 0x01  # IO direction B - 1= input 0 = output
    # Input polarity A - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLA = 0x02
    # Input polarity B - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLB = 0x03
    # The GPINTEN register controls the interrupt-onchange feature for each
    # pin on port A.
    GPINTENA = 0x04
    # The GPINTEN register controls the interrupt-onchange feature for each
    # pin on port B.
    GPINTENB = 0x05
    # Default value for port A - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALA = 0x06
    # Default value for port B - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALB = 0x07
    # Interrupt control register for port A.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONA = 0x08
    # Interrupt control register for port B.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONB = 0x09
    IOCON = 0x0A  # see datasheet for configuration register
    GPPUA = 0x0C  # pull-up resistors for port A
    GPPUB = 0x0D  # pull-up resistors for port B
    # The INTF register reflects the interrupt condition on the port A pins of
    # any pin that is enabled for interrupts. A set bit indicates that the
    # associated pin caused the interrupt.
    INTFA = 0x0E
    # The INTF register reflects the interrupt condition on the port B pins of
    # any pin that is enabled for interrupts.  A set bit indicates that the
    # associated pin caused the interrupt.
    INTFB = 0x0F
    # The INTCAP register captures the GPIO port A value at the time the
    # interrupt occurred.
    INTCAPA = 0x10
    # The INTCAP register captures the GPIO port B value at the time the
    # interrupt occurred.
    INTCAPB = 0x11
    GPIOA = 0x12  # data port A
    GPIOB = 0x13  # data port B
    OLATA = 0x14  # output latches A
    OLATB = 0x15  # output latches B

    # variables
    __port_a_direction = 0x00
    __port_b_direction = 0x00

    __port_a_value = 0x00
    __port_b_value = 0x00

    __port_a_pullup = 0x00
    __port_b_pullup = 0x00

    __port_a_polarity = 0x00
    __port_b_polarity = 0x00

    __ioaddress = 0x20  # I2C address
    __inta = 0x00  # interrupt control for port a
    __intb = 0x00  # interrupt control for port a
    # initial configuration - see IOCON page in the MCP23017 datasheet for
    # more information.
    __ioconfig = 0x22
    __helper = None
    __bus = None

    def __init__(self, reset=True):
        """
        init object with i2c address, default is 0x20, 0x21 for IOPi board,
        load default configuration
        """
        self.__helper = _ABEHelpers()

        self.__bus = self.__helper.get_smbus()
        self.__bus.write_byte_data(
            self.__ioaddress, self.IOCON, self.__ioconfig)
        self.__port_a_value = self.__bus.read_byte_data(
            self.__ioaddress, self.GPIOA)
        self.__port_b_value = self.__bus.read_byte_data(
            self.__ioaddress, self.GPIOB)
        if reset is True:
            self.__bus.write_byte_data(self.__ioaddress, self.IODIRA, 0xFF)
            self.__bus.write_byte_data(self.__ioaddress, self.IODIRB, 0xFF)
            self.set_port_pullups(0, 0x00)
            self.set_port_pullups(1, 0x00)
            self.invert_port(0, 0x00)
            self.invert_port(1, 0x00)

        return

    # local methods
    @staticmethod
    def __checkbit(byte, bit):
        """ internal method for reading the value of a single bit
        within a byte """
        value = 0
        if byte & (1 << bit):
            value = 1
        return value

    # public methods

    def set_pin_direction(self, pin, direction):
        """
         set IO direction for an individual pin
         pins 1 to 16
         direction 1 = input, 0 = output
         """
        pin = pin - 1
        if pin < 8:
            self.__port_a_direction = self.__helper.updatebyte(
                self.__port_a_direction, pin, direction)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRA, self.__port_a_direction)
        else:
            self.__port_b_direction = self.__helper.updatebyte(
                self.__port_b_direction, pin - 8, direction)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRB, self.__port_b_direction)
        return

    def set_port_direction(self, port, direction):
        """
        set direction for an IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        1 = input, 0 = output
        """

        if port == 1:
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRB, direction)
            self.__port_b_direction = direction
        else:
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRA, direction)
            self.__port_a_direction = direction
        return

    def get_port_direction(self, port):
        """
        get the direction from an IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        if port == 1:
            self.__port_b_direction = self.__bus.read_byte_data(
                self.__ioaddress, self.IODIRB)
            return self.__port_b_direction
        else:
            self.__port_a_direction = self.__bus.read_byte_data(
                self.__ioaddress, self.IODIRA)
            return self.__port_a_direction
        return

    def set_pin_pullup(self, pin, value):
        """
        set the internal 100K pull-up resistors for an individual pin
        pins 1 to 16
        value 1 = enabled, 0 = disabled
        """
        pin = pin - 1
        if pin < 8:
            self.__port_a_pullup = self.__helper.updatebyte(
                self.__port_a_pullup, pin, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPPUA, self.__port_a_pullup)
        else:
            self.__port_b_pullup = self.__helper.updatebyte(
                self.__port_b_pullup, pin - 8, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPPUB, self.__port_b_pullup)
        return

    def set_port_pullups(self, port, value):
        """
        set the internal 100K pull-up resistors for the selected IO port
        """
        if port == 1:
            self.__port_b_pullup = value
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUB, value)
        else:
            self.__port_a_pullup = value
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUA, value)
        return

    def get_port_pullups(self, port):
        """
        get the internal pull-up status for the selected IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        if port == 1:
            self.__port_b_pullup = self.__bus.read_byte_data(
                self.__ioaddress, self.GPPUB)
            return self.__port_b_pullup
        else:
            self.__port_a_pullup = self.__bus.read_byte_data(
                self.__ioaddress, self.GPPUA)
            return self.__port_a_pullup
        return

    def write_pin(self, pin, value):
        """
        write to an individual pin 1 - 16
        """

        pin = pin - 1
        if pin < 8:
            self.__port_a_value = self.__helper.updatebyte(
                self.__port_a_value, pin, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPIOA, self.__port_a_value)
        else:
            self.__port_b_value = self.__helper.updatebyte(
                self.__port_b_value, pin - 8, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPIOB, self.__port_b_value)
        return

    def write_port(self, port, value):
        """
        write to all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 1:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOB, value)
            self.__port_b_value = value
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOA, value)
            self.__port_a_value = value
        return

    def read_pin(self, pin):
        """
        read the value of an individual pin 1 - 16
        returns 0 = logic level low, 1 = logic level high
        """
        value = 0
        pin = pin - 1
        if pin < 8:
            self.__port_a_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOA)
            value = self.__checkbit(self.__port_a_value, pin)
        else:
            pin = pin - 8
            self.__port_b_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOB)
            value = self.__checkbit(self.__port_b_value, pin)
        return value

    def read_port(self, port):
        """
        read all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        returns number between 0 and 255 or 0x00 and 0xFF
        """
        value = 0
        if port == 1:
            self.__port_b_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOB)
            value = self.__port_b_value
        else:
            self.__port_a_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOA)
            value = self.__port_a_value
        return value

    def invert_port(self, port, polarity):
        """
        invert the polarity of the pins on a selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """

        if port == 1:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLB, polarity)
            self.__port_b_polarity = polarity
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLA, polarity)
            self.__port_a_polarity = polarity
        return

    def get_port_polarity(self, port):
        """
        get the polarity for the selected IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        if port == 1:
            self.__port_b_polarity = self.__bus.read_byte_data(
                self.__ioaddress, self.IPOLB)
            return self.__port_b_pullup
        else:
            self.__port_a_polarity = self.__bus.read_byte_data(
                self.__ioaddress, self.IPOLA)
            return self.__port_a_pullup
        return

    def invert_pin(self, pin, polarity):
        """
        invert the polarity of the selected pin
        pins 1 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """

        pin = pin - 1
        if pin < 8:
            self.__port_a_polarity = self.__helper.updatebyte(
                self.__port_a_polarity,
                pin,
                polarity)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IPOLA, self.__port_a_polarity)
        else:
            self.__port_b_polarity = self.__helper.updatebyte(
                self.__port_b_polarity,
                pin - 8,
                polarity)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IPOLB, self.__port_b_polarity)
        return

    def mirror_interrupts(self, value):
        """
        1 = The INT pins are internally connected, 0 = The INT pins are not
        connected. __inta is associated with PortA and __intb is associated
        with PortB
        """

        if value == 0:
            self.__ioconfig = self.__helper.updatebyte(self.__ioconfig, 6, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.__ioconfig = self.__helper.updatebyte(self.__ioconfig, 6, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        return

    def set_interrupt_polarity(self, value):
        """
        This sets the polarity of the INT output pins
        1 = Active-high.
        0 = Active-low.
        """

        if value == 0:
            self.__ioconfig = self.__helper.updatebyte(self.__ioconfig, 1, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.__ioconfig = self.__helper.updatebyte(self.__ioconfig, 1, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        return

    def set_interrupt_type(self, port, value):
        """
        Sets the type of interrupt for each pin on the selected port
        1 = interrupt is fired when the pin matches the default value, 0 =
        the interrupt is fired on state change
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONB, value)
        return

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite from the register bit, an
        interrupt occurs.
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALB, value)
        return

    def set_interrupt_on_port(self, port, value):
        """
        Enable interrupts for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENA, value)
            self.__inta = value
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENB, value)
            self.__intb = value
        return

    def set_interrupt_on_pin(self, pin, value):
        """
        Enable interrupts for the selected pin
        Pin = 1 to 16
        Value 0 = interrupt disabled, 1 = interrupt enabled
        """

        pin = pin - 1
        if pin < 8:
            self.__inta = self.__helper.updatebyte(self.__inta, pin, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPINTENA, self.__inta)
        else:
            self.__intb = self.__helper.updatebyte(self.__intb, pin - 8, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPINTENB, self.__intb)
        return

    def read_interrupt_status(self, port):
        """
        read the interrupt status for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFB)
        return value

    def read_interrupt_capture(self, port):
        """
        read the value from the selected port at the time of the last
        interrupt trigger
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPB)
        return value

    def reset_interrupts(self):
        """
        Reset the interrupts A and B to 0
        """

        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return


class RTC:

    """
    Based on the Maxim DS1307

    Define registers values from datasheet
    """
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYOFWEEK = 0x03
    DAY = 0x04
    MONTH = 0x05
    YEAR = 0x06
    CONTROL = 0x07

    # variables
    __rtcaddress = 0x68  # I2C address
    # initial configuration - square wave and output disabled, frequency set
    # to 32.768KHz.
    __rtcconfig = 0x03
    # the DS1307 does not store the current century so that has to be added on
    # manually.
    __century = 2000

    __helper = None
    __bus = None

    # local methods

    def __init__(self):
        self.__helper = _ABEHelpers()
        self.__bus = self.__helper.get_smbus()
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    @staticmethod
    def __bcd_dec(bcd):
        return bcd - 6 * (bcd >> 4)

    @staticmethod
    def __dec_bcd(dec):
        """
        internal method for converting decimal formatted number to BCD
        """
        bcd = 0
        for vala in (dec // 10, dec % 10):
            for valb in (8, 4, 2, 1):
                if vala >= valb:
                    bcd += 1
                    vala -= valb
                bcd <<= 1
        return bcd >> 1

    @staticmethod
    def __get_century(val):
        if len(val) > 2:
            year = val[0] + val[1]
            __century = int(year) * 100
        return

    # public methods
    def set_date(self, date):
        """
        set the date and time on the RTC
        date must be in ISO 8601 format - YYYY-MM-DDTHH:MM:SS
        """

        newdate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        self.__get_century(date)
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.SECONDS,
                                   self.__dec_bcd(newdate.second))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.MINUTES,
                                   self.__dec_bcd(newdate.minute))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.HOURS,
                                   self.__dec_bcd(newdate.hour))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.DAYOFWEEK,
                                   self.__dec_bcd(newdate.weekday()))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.DAY,
                                   self.__dec_bcd(newdate.day))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.MONTH,
                                   self.__dec_bcd(newdate.month))
        self.__bus.write_byte_data(self.__rtcaddress,
                                   self.YEAR,
                                   self.__dec_bcd(newdate.year -
                                                  self.__century))
        return

    def read_date(self):
        """
        read the date and time from the RTC in ISO 8601 format -
        YYYY-MM-DDTHH:MM:SS
        """

        readval = self.__bus.read_i2c_block_data(self.__rtcaddress, 0, 7)
        date = ("%02d-%02d-%02dT%02d:%02d:%02d" % (self.__bcd_dec(readval[6]) +
                                                   self.__century,
                                                   self.__bcd_dec(readval[5]),
                                                   self.__bcd_dec(readval[4]),
                                                   self.__bcd_dec(readval[2]),
                                                   self.__bcd_dec(readval[1]),
                                                   self.__bcd_dec(readval[0])))
        return date

    def enable_output(self):
        """
        Enable the output pin
        """

        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 7, 1)
        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 4, 1)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 7, 0)
        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 4, 0)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def set_frequency(self, frequency):
        """
        set the frequency of the output pin square-wave
        options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        """

        if frequency == 1:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 2:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 3:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 1)
        if frequency == 4:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 1)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def write_memory(self, address, valuearray):
        """
        write to the memory on the ds1307
        the ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes
        variables are:
        address: 0x08 to 0x3F
        valuearray: byte array containing data to be written to memory
        """

        if address >= 0x08 and address <= 0x3F:
            if address + len(valuearray) <= 0x3F:
                self.__bus.write_i2c_block_data(
                    self.__rtcaddress, address, valuearray)
            else:
                raise ValueError('write_memory: memory overflow error: address + \
                                length exceeds 0x3F')
        else:
            raise ValueError('write_memory: address out of range')

    def read_memory(self, address, length):
        """
        read from the memory on the ds1307
        the ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes
        variables are:
        address: 0x08 to 0x3F
        length: up to 32 bytes.  length can not exceed the address space.
        """

        if address >= 0x08 and address <= 0x3F:
            if address <= (0x3F - length):
                return self.__bus.read_i2c_block_data(self.__rtcaddress,
                                                      address, length)
            else:
                raise ValueError('read_memory: memory overflow error: address + \
                                length exceeds 0x3F')
        else:
            raise ValueError('read_memory: address out of range')
