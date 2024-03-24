#!/usr/bin/env python3
import serial
from time import sleep,strftime
from logging import *
from logging.handlers import TimedRotatingFileHandler
#from logger import Logger
from pathlib import Path

# Interfaces with IMCS embedded unit, which abstracts temperature, voltage, current, power, switch state, analog data (PAR)

class ADCInterface:

    def __init__(self,serial_port,baudrate):
        self.device = serial_port
        self.baudrate = baudrate
        self.log_dir = "D:\\logs"
        self.data_dir = "D:\\data"
        self.adc_id = "02"
#       self.sys_logger = Logger("IMCS System Core Logger",f"{self.log_dir}\\sys","imcs_system_core")

    def read_adc_ch(self,ch=0):
#        self.sys_logger.log.info(f"[o] Executing Command: {cmd}")
        cmd = f"#{self.adc_id}{ch}\r\n"
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
            try:
                imcs.write(cmd.encode())
                msg = imcs.readline()[1:].decode().strip("\r")
                print(float(msg))
            except:
                pass

            imcs.flushInput()
            
if __name__ == '__main__':
    g = ADCInterface("COM24",9600)
    while True:
        g.read_adc_ch()
        sleep(0.1)
    pass
