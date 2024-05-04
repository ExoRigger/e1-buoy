#!/usr/bin/env python3

from lib.core_control.logger import Logger
from lib.core_control.core import Core
import datetime
from time import sleep
import sys


# Directory locations for input configuration files & output log and data files
CONF_DIR = ""
LOG_DIR = "C:\\core_supervisor\\logs"
DATA_DIR = "C:\\core_supervisor\\data"

# Directory location for the supevisor logs
supervisor_log_dir = LOG_DIR + "\\supervisor_logs"


# ================================================================
# Overwatches core control of PML E1 Systems
# ================================================================

def main():
    master_log =  Logger("supervisor_log",supervisor_log_dir,"supervisor_log")
    master_log.log.info(f"[+] Core System Supervisor Active")
    e1_core = Core(LOG_DIR)

    try:
        ret = e1_core.run()
        if ret == 1:
            sys.exit() 
    except Exception as E:
        master_log.log.info(f"[-] Core System Failure: {E}")


if __name__ == '__main__':
    main()
