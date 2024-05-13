#!/usr/bin/env python3

# =====================================================================
# This class is an interface for controlling multiple attached payloads
# and handles data collection to a specified data directory
# =====================================================================

import threading
from time import sleep
import sys
import datetime
from lib.core_control.logger import Logger
from lib.payload_control.wqm.wqm_control_interface import WQMControlInterface

class IMCPayloadInterface:
    # The constructor initializes MCU communication parameters and
    # creates a logging object to store system activity
    #   Constructor inputs: 
    #    data_dir:
    def __init__(self,log_dir,data_dir):
        self.log_dir = log_dir + "\\pyl"
        self.data_dir = data_dir
        self.pyl_log = Logger("payload_log",self.log_dir,"pyl_log")
        self.pyl_log.log.info(f"[+] (PYL Control) INITIALIZED")

    # TODO: Spawn asynchonous thread for each instrument to log data to, give each object self.pyl_log_dir to store their data
    def sample_pyl(self):
        # self.ctd_ctl = WQMControlInterface("COM",19200) 
        # MET MAAT Instrument data monitor here
        self.pyl_log.log.info(f"[o] (PYL Control): ACTIVE")
        self.pyl_log.log.info(f"[o] (PYL Control): SAMPLE PYL")
        #wqm_control = WQMControlInterface("COM",19200)
        #wqm_control.run() # In future, augment this to do the same as the IMC power controller
        sleep(30)
        self.pyl_log.log.info(f"[+] (PYL Control): SAMPLE PYL")
        self.pyl_log.log.info(f"[o] (PYL Control): END")
