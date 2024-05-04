#!/usr/bin/env python3

# setup data manager and power monitor
import threading
from time import sleep
import sys
import datetime
from lib.core_control.logger import Logger
from lib.core_control.imc_control import IMCSPowerInterface

class Core:

    def __init__(self,log_dir):
        # Setup logging and transmission of data
        self.log_output = log_dir 
        self.sys_log_dir = self.log_output + "\\system_logs"
        self.pyl_log_dir = self.log_output + "\\payload_logs"
        self.init_logging()
        
        # Parse config, which involves using core_ctl to set power channels accordingly


# prepend /mnt/d to logging dirs
    def init_logging(self):
        self.sys_log = Logger("system_log",self.sys_log_dir + "\\sys","sys_log")
        self.sys_log.log.info(f"[+] Core System Logging Initialized")
        
        self.pyl_log = Logger("payload_log",self.pyl_log_dir,"pyl_log")
        self.pyl_log.log.info(f"[+] Payload Instrument Logging Initialized")

        self.sys_log.log.info(f"[+] Core System Logging Initialized")
        
    def run(self):
        core_thread = threading.Thread(target=self.run_core_ctl).start()
        instr_thread  = threading.Thread(target=self.run_inst_ctl).start()

    # TODO: Spawn asynchonous thread for each instrument to log data to, give each object self.pyl_log_dir to store their data
    # ----------THREADS----------------------------------------------------------------- #
    def run_core_ctl(self):
        self.core_ctl = IMCSPowerInterface("COM6",115200,self.sys_log_dir)
        self.sys_log.log.info(f"[+] Core Control Active")
        # Get system data from core
        
        self.sys_log.log.info(f"[o] Sampling IMC")
        while True:
            self.core_ctl.sample_imc()
            sleep(0.5)


    def run_inst_ctl(self):
        # self.ctd_ctl = WQMControlInterface("/dev/ttyUSB0",19200) # Change this to a windows port  
        # MET MAAT Instrument data monitor here
        
        self.pyl_log.log.info(f"[+] Instrument Control Active")
        
        # self.pyl_log.log.info(f"[o] Engaging CTD")
        
        while True:
            sleep(0.5)

           

    # --------------------------------------------------------------------------- #
