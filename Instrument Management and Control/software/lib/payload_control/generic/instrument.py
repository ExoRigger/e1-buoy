#!/usr/bin/env python3

#################################################################################
# Instrument module - Contains classes for defining and interfacing with generic
# instruments - Inactive
#################################################################################

from time import sleep
from serial import Serial
from pkg_imcs_power_manager.logger import *

################################################################################
# Instrument Class: Handles low level GPIO function between each individual 
# instrument
################################################################################
class Instrument():

    instr_logger = Logger("instrument_debug_logs",".","instruments")
    log_inst = instr_logger.log



    def __init__(self,label,pin,state):
        self.name = label # Idk why but getattr() doesnt work unless I have this
        self.label = label # 15 Character limit for instrument labels
        self.pin = int(pin)
        self.state = state # Will change every time GPIO pin is read
        self.current = 0 # Will probably be set using pandas on a separate file
        self.data_dir = ""

        self.log_inst.debug(f"[*] Initializing Instrument {self.label}")


  ################################################################################
  # Update attributes of a instrument
  ################################################################################
    def update(self,new_state,new_current): # Add parameter for channel (pin)
        self.state = new_state
        self.current = new_current
        return

  ################################################################################
  # Display status of instrument 
  ################################################################################
    def status(self):
        # log_inst.debug(f"{YEL}[*] Displaying status of {self.label}") 
        if not self.state:
            print(f"+--------------------------------------------------------+\n\
|[-] OFF  \t  {self.label:<15}\t -o      o- \t |\n\
+--------------------------------------------------------+")

        elif self.state:
             print(f"+--------------------------------------------------------+\n\
|[+] ON  \t {self.label:<15}\t -o------o- \t |\n\
{GRN}+--------------------------------------------------------+")

        else:
            self.log_inst.error(f"[-] Error reading status of {self.label}")
            pass


  ################################################################################
  # Power off instrument, wait 10 seconds and power on
  ################################################################################
    def power_cycle(self):
        # Open serial connection and send cycle pin to arduino
        self.log_inst.debug(f"{YEL}[*] Power cycling {self.label} {EF} \n\n")
        try:
            self.state = 0
            self.status()
            
            sleep(10)
            self.state = 1
            self.status()
            self.log_inst.debug(f"{GRN}[+] Success {EF}")
            sleep(1)

        except Exception as error:
            self.log_inst.error(f"{RED} [-] Error power cycling {self.label}: {error} {EF} \n\n")
            pass
        return
