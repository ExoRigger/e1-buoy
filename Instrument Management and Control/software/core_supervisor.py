#!/usr/bin/env python3

from lib.core_control.logger import Logger
from lib.core_control.core import Core
import datetime
from time import sleep
import sys

LOG_DIR = "C:\core_supervisor\logs"
DATA_DIR = "C:\core_supervisor\data"

master_log_dir = LOG_DIR + "\master"

# Any master/sysadmin functions beyond core control in here


def main():
    master_log =  Logger("master_log",master_log_dir,"master_log")
    master_log.log.info(f"[o] Core Supervisor Engaged - Initiating Core System")
    l4_core = Core(LOG_DIR)

    try:

        ret = l4_core.run()
        if ret == 1:
            sys.exit()
            
    except Exception as E:

        master_log.log.info(f"[-] Core System Failure: {E}")


if __name__ == '__main__':


    main()
