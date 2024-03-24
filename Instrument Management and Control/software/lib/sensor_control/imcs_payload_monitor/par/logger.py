#!/usr/bin/env python3

from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG
from logging.handlers import TimedRotatingFileHandler
from time import strftime
from pathlib import Path


class Logger:

    def __init__(self,label,location,filename):
      # Params
        self.label = label
        self.location = location
        self.filename = filename

      # Create Dir if not exists
        p = Path(self.location).mkdir(parents=True,exist_ok=True)

        self.log = getLogger(self.label)
        self.log.setLevel(DEBUG)
        formatter2 = Formatter('%(asctime)s: %(funcName)s (%(lineno)d): %(message)s', '%H:%M:%S')
        formatter = Formatter('%(asctime)s: %(message)s', '%H:%M:%S')

      # Handle logging to file and stdout
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

        logfile_handler = TimedRotatingFileHandler(strftime(f"{self.location}/{self.filename}_%Y-%m-%d_%H%M%S.log"), when="h",interval=1,backupCount=100)
        logfile_handler.setFormatter(formatter)
        self.log.addHandler(logfile_handler)


def main():
     l = Logger("Logger Test","./logger_test","logger")

if __name__ == '__main__':
    main()
