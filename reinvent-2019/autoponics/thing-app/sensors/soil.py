from .sensor import Sensor
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class SoilSensor(Sensor):
    def __init__(self):
        Sensor.__init__(self)

        self.moisture_min = float(self.config["soil"]["min"])
        self.moisture_max = float(self.config["soil"]["max"])

        # create SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D8)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        
        # create an analog input channel
        self.pin = []
        self.pin.append(AnalogIn(mcp, MCP.P0))
        self.pin.append(AnalogIn(mcp, MCP.P1))
        self.pin.append(AnalogIn(mcp, MCP.P2))
        self.pin.append(AnalogIn(mcp, MCP.P3))
        self.pin.append(AnalogIn(mcp, MCP.P4))
        self.pin.append(AnalogIn(mcp, MCP.P5))
        self.pin.append(AnalogIn(mcp, MCP.P6))
        self.pin.append(AnalogIn(mcp, MCP.P7))

    def read(self, no):
        return 100 - self.normalize(
            self.moisture_min,
            self.moisture_max,
            self.pin[no].value
        )

    def read_raw(self, no):
        return self.pin[no].value
