#!/usr/bin/env python3
import serial
from time import sleep,strftime
from logging import *
from logging.handlers import TimedRotatingFileHandler
from lib.core_control.logger import Logger
from pathlib import Path

# Interfaces with IMCS embedded unit, which abstracts temperature, voltage, current, power, switch state, analog data 

class IMCSPowerInterface:

    def __init__(self,serial_port,baudrate):
        self.device = serial_port
        self.baudrate = baudrate
        self.log_dir = ".\logs"
        self.data_dir = ".\data"
        self.sys_logger = Logger("IMCS System Core Logger",f"{self.log_dir}\\sys","imcs_system_core")

    def send_cmd(self,cmd):
        byts = cmd.encode()
        self.sys_logger.log.info(f"[o] Executing Command: {byts}")
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:

            sleep(0.1)
            imcs.write(byts)
            
            while imcs.inWaiting():
                l = imcs.readline().decode()
                
            imcs.flushInput()
            
    
    def cycle_ch(self,ch):
        pass
        
        
    def toggle_ch(self,ch):
        pass
    
    def set_mode(self,mode):
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:

            sleep(0.1)
            cmd = f"m\r{mode}\r"
            imcs.write(cmd.encode())
            
            while imcs.inWaiting():
                l = imcs.readline().decode()
            imcs.flushInput()
           
    def log_status(self,status_string):
        ch_array = status_string.split(';')
        self.sys_logger.log.info("CHANNEL,STATE,VOLTAGE,CURRENT")
        for ch in ch_array:
            self.sys_logger.log.info(ch)
        
        
    def sample_imc(self,samples=200):
        
        self.set_mode("1")
        self.set_mode("1")
        for i in range(samples):
            try:
                with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
                            l = imcs.readline().decode()
                            self.log_status(l)
                            sleep(0.2)
                            
            except Exception as Err:
                print("err")
        self.set_mode("0")
        self.set_mode("0")
        
if __name__ == '__main__':
    g = IMCSPowerInterface("COM4",115200) # Change this
    g.sample_imc()

        
