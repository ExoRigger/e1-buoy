#!/usr/bin/env python3

# =====================================================================
# This class is an interface for managing supply power to attached
# payloads via the IMC microcontroller and logs 
# power control actions and power information of each payload streamed 
# from the MCU.
# =====================================================================

import serial
from time import sleep,strftime
from logging import *
from logging.handlers import TimedRotatingFileHandler
from lib.core_control.logger import Logger
from pathlib import Path

class IMCPowerInterface:
    # The constructor initializes MCU communication parameters and
    # creates a logging object to store system activity
    #   Constructor inputs: 
    #    serial_port: Serial port of MCU
    #    baudrate:    Telemetry baudrate of MCU
    def __init__(self,serial_port,baudrate,log_dir,data_dir,payloads):
        self.device = serial_port
        self.baudrate = baudrate
        self.log_dir = log_dir + "\\imc"
        self.data_dir = data_dir
        self.payloads = payloads
        self.imc_control_logger = Logger("IMC System Logger",f"{self.log_dir}","imc_control_log")
        self.imc_power_logger = Logger("IMC Power Logger",f"{self.log_dir}" + "\\power_logs","imc_power_log")
        self.par_logger = Logger("PAR Sensor Logger",self.data_dir + "\\par","par")
        
        self.par_logger.log.info(f"PAR")
        self.imc_power_logger.log.info(f"CHANNEL,STATE,VOLTAGE(V),CURRENT(mA)")
        
        self.imc_control_logger.log.info(f"[o] (IMC Control) INITIALIZED")
        
    # Initiate a telemetry session with the MCU to send a command
    #   Function inputs:
    #     cmd: 
    def send_data(self,data):
        self.imc_control_logger.log.info(f"[o] (IMC Control) TX: {data}")
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
            imcs.write(data.encode())
           
            while imcs.inWaiting():
                ack = imcs.readline().decode()
                self.imc_control_logger.log.info(f"[o] (IMC Control) RX: {ack}")
                
            imcs.flushInput()
            imcs.flushOutput()
        
    def log_data(self,data):
        ch_array = data.split(';')
        par = ch_array[-1].strip()
        
        for ch in ch_array[:-1]:
            self.imc_power_logger.log.info(ch)
            self.par_logger.log.info(par)
  
    # ================================================================    
    # Abstracted IMC Commands to reduce direct access to MCU interface
    # ================================================================
    
    def set_ch(self,ch,state):
        self.imc_control_logger.log.info(f"[o] (IMC Control) SET: {ch} {state}")
        cmd1 = f"s\r"
        cmd2 = f"{ch}\r"
        cmd3 = f"{state}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.send_data(cmd3)  
        self.imc_control_logger.log.info(f"[+] (IMC Control) SET: {ch} {state}")
        
    def cycle_ch(self,ch):
        self.imc_control_logger.log.info(f"[o] (IMC Control) CYCLE: {ch}")
        cmd1 = f"c\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) CYCLE: {ch}")
        
    def toggle_ch(self,ch):
        self.imc_control_logger.log.info(f"[o] (IMC Control) TOGGLE: {ch}")
        cmd1 = f"t\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) TOGGLE: {ch}")
    
    def set_mode(self,mode):
        self.imc_control_logger.log.info(f"[o] (IMC Control) MODE: {mode}")
        cmd1 = f"m\r"
        cmd2 = f"{mode}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) MODE: {mode}")
 
    def activate_pyl(self):
        self.set_ch(3,1)
        self.set_ch(4,1)
        self.imc_control_logger.log.info(f"[+] (IMC Control) PYL ACTIVE")
      
    def sample_imc(self,samples=200,frequency=5):
        dt = 1/frequency
        self.set_mode("1")
        self.imc_control_logger.log.info(f"[o] (IMC Control) ACTIVE")  
        self.imc_control_logger.log.info(f"[o] (IMC Control) SAMPLE IMC")
        self.activate_pyl()
        for i in range(samples):
            try:
                sleep(dt)
                with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
                            status_string = imcs.readline().decode()
                self.log_data(status_string)                         
            except Exception as Err:
                self.imc_control_logger.log.info(f"[-] (IMC Control) SAMPLE IMC \n{Err}")
        self.set_mode("0")
        self.imc_control_logger.log.info(f"[+] (IMC Control) SAMPLE IMC")
        self.deactivate_pyl()
        self.imc_control_logger.log.info(f"[o] (IMC Control) END")      
              
    def deactivate_pyl(self):
        self.set_ch(3,0)
        self.set_ch(4,0)
        self.imc_control_logger.log.info(f"[+] (IMC Control) PYL DISABLED")
    # ================================================================
    
if __name__ == '__main__':
    g = IMCPowerInterface("COM6",115200) # Change this
    g.sample_imc()

        
