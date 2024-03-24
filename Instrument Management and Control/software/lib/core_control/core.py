#!/usr/bin/env python3

# setup data manager and power monitor
import threading
from time import sleep
import sys
import datetime
from lib.core_control.logger import Logger
from lib.core_control.imc_control import IMCSPowerInterface

class Core:

  # Setup logging and transmission of data
    def __init__(self,log_dir):
        self.log_output = log_dir 
#       self.ctd_ctl = WQMControlInterface("/dev/ttyUSB0",19200) # Change this to a windows port
        self.init_logging()
        # Parse config, which involves using core_ctl to set power channels accordingly


# prepend /mnt/d to logging dirs
    def init_logging(self):

        core_log_dir = self.log_output + "\core"
        inst_log_dir = self.log_output + "\instruments"

        self.sys_log = Logger("system_log",core_log_dir,"sys_log")
        self.sys_log.log.info(f"[+] Core System Logging Active")
        
        self.inst_log = Logger("instrument_log",inst_log_dir,"instr_log")
        self.inst_log.log.info(f"[+] Payload Instrument Logging Active")

        self.sys_log.log.info(f"[+] Core System Logging Initialized")
        
    def run(self):
        core_thread = threading.Thread(target=self.run_core_ctl).start()
        instr_thread  = threading.Thread(target=self.run_inst_ctl).start()


    # ----------THREADS----------------------------------------------------------------- #
    def run_core_ctl(self):
        self.core_ctl = IMCSPowerInterface("COM4",115200)
        self.sys_log.log.info(f"[+] Core Control Active")
        # Get system data from core
        self.core_ctl.sample_imc()
        sleep(0.5)

    def run_inst_ctl(self):
        self.inst_log.log.info(f"[o] Engaging Instrument Control")
        while True:
            sleep(0.5)

           

    # --------------------------------------------------------------------------- #
