import configparser
import os

class MyUptimeConfig:
    def __init__(self, filename) -> None:
        self.configFile = filename
        self.home = os.path.expanduser("~")
        self.inifile = self.home + "/"  + self.configFile
        self.config = configparser.ConfigParser()
        self.config.read(self.inifile)

    def getKey(self, key, val):
        try:
            return self.config[key][val]
        except KeyError:
            return ""