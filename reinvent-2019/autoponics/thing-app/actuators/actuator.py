import os
import configparser

class Actuator():
    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, "../config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)
        if self.config == []:
            raise OSError(2, "No such file or directory", "config.ini")

        self.status = False

    def on(self):
        self.status = True

    def off(self):
        self.status = False
