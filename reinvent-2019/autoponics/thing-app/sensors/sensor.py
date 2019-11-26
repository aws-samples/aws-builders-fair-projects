import os
import configparser

class Sensor():
    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, "../config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)
        if self.config == []:
            raise OSError(2, "No such file or directory", "config.ini")

    def read(self):
        raise NotImplementedError

    def read_raw(self):
        raise NotImplementedError        

    def normalize(self, minimum, maximum, value):
        raw_value = ((value - minimum) / (maximum - minimum)) * 100
        return (raw_value if raw_value < 100 else 100.0) if raw_value > 0 else 0.0
