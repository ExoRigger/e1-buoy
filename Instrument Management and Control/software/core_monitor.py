#!/usr/bin/env python3

# ================================================================
# Wrapper scrpt for overwatching core control of PML E1 Buoy
# Power management and data acquisition systems
# ================================================================

from lib.core_control.logger import Logger
from lib.core_control.imc_core import Core
import datetime
from time import sleep
import sys

# Directory locations for input configuration files & output log and data files
CONF_DIR = ".\\conf"
LOG_DIR = "C:\\E1_InstrumentControl\\system_logs"
DATA_DIR = "C:\\E1_InstrumentControl\\payload_data"

# Directory location for the supevisor logs

def imcCoreMonitor():
    core_mon_logger =  Logger("core_mon_log",LOG_DIR + "\\core_monitor","imc_core_monitor")
    core_mon_logger.log.info(f"[o] (Core Monitor) INITIALIZED")
    e1_core = Core(CONF_DIR,LOG_DIR,DATA_DIR)
 
    try:
        core_mon_logger.log.info(f"[o] (Core Monitor) ACTIVE")
        core_return_status = e1_core.run()
        if core_return_status == 0:
            core_mon_logger.log.info(f"[+] (Core Monitor) END")
            
        elif core_return_status == 1:
            sys.exit() 
        
    except Exception as E:
        core_mon_logger.log.error(f"[-] (Core Monitor) CORE FAILURE: {E}")
        
    
    
    
if __name__ == '__main__':

    imcCoreMonitor()
