#!/usr/bin/env python
"""
================================================
ABElectronics RTC Pi Real-time clock

Requires smbus2 or python smbus to be installed
================================================
"""
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
import re
import platform
import datetime


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

    __bus = None

    # local methods

    @staticmethod
    def __get_smbus():
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

    @staticmethod
    def __updatebyte(byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """

        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

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

    def __init__(self):
        self.__bus = self.__get_smbus()
        self.__bus.write_byte_data(self.__rtcaddress, self.CONTROL,
                                   self.__rtcconfig)
        return

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

        self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 7, 1)
        self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 4, 1)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 7, 0)
        self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 4, 0)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def set_frequency(self, frequency):
        """
        set the frequency of the output pin square-wave
        options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        """

        if frequency == 1:
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 2:
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 3:
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 1, 1)
        if frequency == 4:
            __rtcconfig = self.__updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__updatebyte(self.__rtcconfig, 1, 1)
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
