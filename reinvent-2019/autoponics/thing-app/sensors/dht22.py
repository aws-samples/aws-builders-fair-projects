from .sensor import Sensor
import board
import Adafruit_DHT as adafruit_dht

class DHT22Sensor(Sensor):
    def __init__(self):
        Sensor.__init__(self)

        self.dht22 = adafruit_dht.DHT22

    def read(self):
        return self.read_raw()

    def read_raw(self):
        return adafruit_dht.read_retry(self.dht22, 4)
