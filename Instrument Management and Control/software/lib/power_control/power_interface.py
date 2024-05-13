#!/usr/bin/env python3

# =====================================================================
# This class is an interface for managing supply power to attached
# payloads via the IMC microcontroller and logs 
# power control actions and power information of each payload streamed 
# from the MCU.
# =====================================================================

import serial
from time import sleep,strftime
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
        
      # Hide data streams from std_out
        self.imc_power_logger.stream_handler.setLevel(100) 
        self.par_logger.stream_handler.setLevel(100)
        
        self.par_logger.log.info(f"PAR")
        self.imc_power_logger.log.info(f"DEVICE,CHANNEL,STATE,VOLTAGE(V),CURRENT(mA)")
        
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
        
        for ch_data in ch_array[:-1]:
            try:
                log_entry = self.payloads[int(ch_data[0])] + "," + ch_data
                self.imc_power_logger.log.info(log_entry)
                self.par_logger.log.info(par)
            except Exception as error:
                #self.imc_control_logger.log.error(f"[-] (IMC Control) ERR: {error}")
                continue

    # ================================================================    
    # Abstracted IMC Commands to reduce direct access to MCU interface
    # ================================================================
    
    def set_ch(self,ch,state):
        device = self.payloads[ch]
        self.imc_control_logger.log.info(f"[o] (IMC Control) SET: {device} {state}")
        cmd1 = f"s\r"
        cmd2 = f"{ch}\r"
        cmd3 = f"{state}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.send_data(cmd3)  
        self.imc_control_logger.log.info(f"[+] (IMC Control) SET: {device} {state}")
        
    def cycle_ch(self,ch):
        device = self.payloads[ch]
        self.imc_control_logger.log.info(f"[o] (IMC Control) CYCLE: {device}")
        cmd1 = f"c\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) CYCLE: {device}")
        
    def toggle_ch(self,ch):
        device = self.payloads[ch]
        self.imc_control_logger.log.info(f"[o] (IMC Control) TOGGLE: {device}")
        cmd1 = f"t\r"
        cmd2 = f"{ch}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) TOGGLE: {device}")
   
  # Set logging mode (0 = poll, 1 = stream)   
    def set_mode(self,mode):
        self.imc_control_logger.log.info(f"[o] (IMC Control) MODE: {mode}")
        cmd1 = f"m\r"
        cmd2 = f"{mode}\r"
        self.send_data(cmd1)
        self.send_data(cmd2)
        self.imc_control_logger.log.info(f"[+] (IMC Control) MODE: {mode}")

  # Power on CTD and PAR 
    def activate_pyl(self):
        self.set_ch(3,1)
        self.set_ch(4,1)
        self.imc_control_logger.log.info(f"[+] (IMC Control) PYL ACTIVE")
      

  # Activates payload, takes 200 samples at 5Hz default, stops logging, deactivates payload  
  # Fails 10% of the time, unknown reason. Possibly due to open/close method instead of open/listen/close
  # Method now detects if no data is received, the function is repeated
    def sample_imc(self,samples=200,frequency=5):
        dt = 1/frequency
        self.imc_control_logger.log.info(f"[o] (IMC Control) ACTIVE")  
        self.imc_control_logger.log.info(f"[o] (IMC Control) SAMPLE IMC")
        self.activate_pyl()
        self.set_mode(1)
        restart_sampling = False
        with serial.Serial(port=self.device,baudrate=self.baudrate,timeout=1) as imcs:
            for i in range(samples):
                try:
                    sleep(dt)
                    status_string = imcs.readline().decode()
                    if not len(status_string):
                        self.imc_control_logger.log.info("[-] (IMC Control) NO DATA FROM IMC")
                        restart_sampling = True
                        break
                    else:
                        self.log_data(status_string)                         
                except Exception as Err:
                    self.imc_control_logger.log.info(f"[-] (IMC Control) SAMPLE IMC \n{Err}")
        self.deactivate_pyl()
        self.set_mode(0)
        self.imc_control_logger.log.info(f"[+] (IMC Control) SAMPLE IMC")
        self.imc_control_logger.log.info(f"[o] (IMC Control) END")      
 
        if restart_sampling:
            self.imc_control_logger.log.info("[x] (IMC Control) RESTART SAMPLING")
            sleep(2)
            self.sample_imc(samples,frequency)
             
  # Power off CTD and PAR
    def deactivate_pyl(self):
        self.set_ch(3,0)
        self.set_ch(4,0)
        self.imc_control_logger.log.info(f"[+] (IMC Control) PYL DISABLED")
    # ================================================================
    
if __name__ == '__main__':
    g = IMCPowerInterface("COM6",115200) # Change this
    g.sample_imc()
