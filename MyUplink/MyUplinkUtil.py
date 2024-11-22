import configparser
import os
import logging
import logging.handlers

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

class myLogger:
    def __init__(self, logfile, version) -> None:
        logger = logging.getLogger('__name__')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s ' + logfile + ' ver:' + str(version) + ' %(levelname)s %(message)s')
        handler = logging.handlers.RotatingFileHandler(logfile + ".log", mode='a', maxBytes=8388608, backupCount=16)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.logfile = logfile

    def getLogger(self):
        self.logger.info("Starting ...")
        return self.logger
    
    def setLoggerLevel(self, level: str):
        goodLevels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        level = level.upper()
        if level in goodLevels:
            self.logger.setLevel(level)
