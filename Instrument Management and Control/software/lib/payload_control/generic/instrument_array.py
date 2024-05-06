#!/usr/bin/env python3

#################################################################################
# InstrumentArray - A module for defining and interfacing with objects of 
# type / derivation of Instrument - Inactive
#################################################################################

from glob import glob
from pandas import read_csv
from pkg_imcs_power_manager.colours import *
from pkg_imcs_power_manager.logger import *
from pkg_imcs_power_manager.instrument import Instrument
import os

class InstrumentArray:
  
    array_logger = Logger(f"instrument_array_debug_logs",".","InstrArray")
    log_array = array_logger.log

    def __init__(self,CFG_FILE):
       # self.rt_log_dir = "/home/power-manager/l4-pmm/logs/instrument_runtime_logs"
       # self.runtime_logger = Logger("instrument_runtime_logs", self.rt_log_dir,"instrument_state")
       # self.log_rt = self.runtime_logger.log

        self.cfg_file = CFG_FILE
        self.instruments = []
        self.log_array.debug(f"{YEL}[*] Initializing Instrument Array {EF}")
        try:
            self.df = read_csv(self.cfg_file,sep=";")
            self.labels = self.df['INSTRUMENT']
            self.pins = self.df['PIN']
            self.states = self.df['STATE']

            for i in range(len(self.labels)): # I don't like the len(self.labels), change it. 
                l,p,s = self.labels[i],self.pins[i],self.states[i]
                self.instruments.append(Instrument(l,p,s))

            self.log_array.debug(f"{GRN}[+] Initialized the following: {EF}\n\n")
            for s in self.instruments:
                self.log_array.debug(f"{GRN}Instrument: {s.label}\nGPIO Assignment: {s.pin}{EF}\n" )
       
        except Exception as err:
            self.log_array.error(f"{RED}[-] Error Initializing Instrument(s): {err}")


  ###############################################################################
  # Execute a method for a particular instrument
  ###############################################################################
    def cmd_device(self,cmd):
        instrument = input(f"{YEL}({cmd}) [input device] >>>{EF} ") 
        self.log_array.debug(f"{YEL}[*] Instructing {BLU}{instrument}{EF} to {BLU}{cmd}{EF}")
        for s in self.instruments:
            if s.label == instrument:
                try:
                    getattr(s,cmd)()
                    self.log_array.debug(f"{GRN}[+] Success{EF}")
                except Exception as err:
                    self.log_array.error(f"Error pushing {cmd} to {instrument}: {err}")


  ###############################################################################
  # Initializes and adds a new instrument
  ###############################################################################
    def add_device(self):
        new_device = input(f"{YEL}(add_device) Name of instrument: {EF}")
        gpio_pin = input(f"{YEL}GPIO Allocation: {EF}")
        self.log_array.debug(f"{YEL}[*] Constructing {BLU}{new_device}{EF} and binding to pin {BLU}{gpio_pin}{EF}")

        self.instruments.append(Instrument(new_device,gpio_pin,0))
        self.log_array.debug(f"{GRN}[+] Done {EF}")

        print(f"{BLU}[o] Instrument is off, toggle to power {EF}")

        
  ###############################################################################
  # Get status of all channels from IMCS and update each instrument's state
  # Give update parameters (which instrument, values to update, i.e. state, current)
  ###############################################################################
    def update(self):
        for ins in self.instruments:
            ins.status()


if __name__ == '__main__':
    print(f"[o] InstrumentArray Test")
