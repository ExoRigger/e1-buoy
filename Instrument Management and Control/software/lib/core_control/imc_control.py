#!/usr/bin/env python3
import serial
from time import sleep,strftime
from logging import *
from logging.handlers import TimedRotatingFileHandler
from lib.core_control.logger import Logger
from pathlib import Path

# Interfaces with IMCS embedded unit, which abstracts temperature, voltage, current, power, switch state, analog data 

class IMCSPowerInterface:
    # The constructor initializes MCU communication parameters and
    # creates a logging object to store system activity
    #   Constructor inputs: 
    #    serial_port: Serial port of MCU
    #    baudrate:    Telemetry baudrate of MCU
    def __init__(self,serial_port,baudrate,log_dir,data_dir):
        self.device = serial_port
        self.baudrate = baudrate
        self.log_dir = log_dir + "\\imc"
        self.data_dir = data_dir
        self.sys_logger = Logger("IMCS System Core Logger",f"{self.log_dir}","imc_power_log")
        self.par_logger = Logger("PAR Sensor Logger",self.data_dir + "\\par","par")

    # Initiate a telemetry session with the MCU to send a command
    #   Function inputs:
    #     cmd: 
    def send_data(self,data):
        self.sys_logger.log.info(f"[o] Sending Data: {data}")
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
            imcs.write(data.encode())
           
            while imcs.inWaiting():
                ack = imcs.readline().decode()
                self.sys_logger.log.info(f"[o] Receiving Data: {ack}")
                
            imcs.flushInput()
            imcs.flushOutput()
        
    def log_data(self,data):
        ch_array = data.split(';')
        par = ch_array[-1]
        self.sys_logger.log.info("CHANNEL,STATE,VOLTAGE,CURRENT")
        for ch in ch_array[:-1]:
            self.sys_logger.log.info(ch)
            self.par_logger.log.info(par)

  
    # ================================================================    
    # Abstracted IMC Commands to reduce direct access to MCU interface
    # ================================================================
    
    def cycle_ch(self,ch):
        cmd1 = f"c\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.sys_logger.log.info(f"[+] Ch {ch} Power Cycled")
        
    def toggle_ch(self,ch):
        cmd1 = f"t\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.sys_logger.log.info(f"[+] Ch {ch} Toggled")
    
    def set_mode(self,mode):
        cmd1 = f"m\r"
        cmd2 = f"{mode}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.sys_logger.log.info(f"[+] IMC Mode Set: {mode}")
 
     
    def sample_imc(self,samples=200,frequency=0.2):
        self.set_mode("1")
        for i in range(samples):
            try:
                sleep(frequency)
                with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
                            status_string = imcs.readline().decode()
                self.log_data(status_string)                         
            except Exception as Err:
                self.sys_logger.log.info(f"[-] Error Sampling IMC: \n{Err}")
        self.set_mode("0")
        
    # ================================================================
if __name__ == '__main__':
    g = IMCSPowerInterface("COM6",115200) # Change this
    g.sample_imc()

        
