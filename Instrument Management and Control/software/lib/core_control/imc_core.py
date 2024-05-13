#!/usr/bin/env python3

# =====================================================================
# This class creates logging objects for power control and data
# acquisition and contains asynchonous threadded control loops for 
# power and payload control
# =====================================================================

import threading
from time import sleep
import sys
import datetime
from lib.core_control.logger import Logger
from lib.power_control.power_interface import IMCPowerInterface
from lib.payload_control.payload_interface import IMCPayloadInterface

class Core:

    def __init__(self,log_dir,data_dir):
        # Define attached payloads
        self.payloads = {
                          1:"PAYLOAD_PC",
                          2:"STEATITE_MMCU",
                          3:"WETLABS_WQM",
                          4:"SEABIRD_PAR",
                        }   
        # Setup logging and collection of data
        self.sys_log_dir = log_dir
        self.pyl_data_dir = data_dir
        self.init_logging()

                                      
    def init_logging(self):
        self.sys_log = Logger("core_logger",self.sys_log_dir + "\\core","core_log")
        self.sys_log.log.info(f"[+] (Core Control) INITIALIZED")
        
    def run(self):
        try:
            self.sys_log.log.info(f"[o] (Core Control) ACTIVE")
            imc_thread = threading.Thread(target=self.run_imc_ctl)           
            pyl_thread  = threading.Thread(target=self.run_pyl_ctl)
            
            imc_thread.start()
            pyl_thread.start()
            
            imc_thread.join()
            pyl_thread.join()
            
            self.sys_log.log.info(f"[o] (Core Control) END")
            return 0
            
        except Exception as error:
            self.sys_log.log.error(error)
            return 1
 
# =====================================================================
# Spin up two separate threads to govern power control and data logging
# =====================================================================
# TODO: Give IMCPowerInterface the list of sensor;channel allocations
    def run_imc_ctl(self):
        self.core_ctl = IMCPowerInterface("COM38",115200,self.sys_log_dir,self.pyl_data_dir,self.payloads)        
        self.core_ctl.sample_imc()

    def run_pyl_ctl(self):
        self.pyl_ctl = IMCPayloadInterface(self.sys_log_dir,self.pyl_data_dir)
        self.pyl_ctl.sample_pyl()
        
# =====================================================================
