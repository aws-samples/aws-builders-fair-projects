from .sensor import Sensor
import busio
import board
import adafruit_veml6075

class UVSensor(Sensor):
    def __init__(self):
        Sensor.__init__(self)

        self.uv_min = float(self.config["uv"]["min"])
        self.uv_max = float(self.config["uv"]["max"])

        # initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)

        # create the VEML6075 object
        self.veml = adafruit_veml6075.VEML6075(
            i2c,
            integration_time=int(self.config["uv"]["integration_time"])
        )

    def read(self):
        return self.normalize(
            self.uv_min,
            self.uv_max,
            self.veml.uv_index
        )

    def read_raw(self):
        return self.veml.uv_index
