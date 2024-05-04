#!/usr/bin/env python3
import serial
import time
from logger import Logger
from pathlib import Path
# Comminicate via serial and monitor


class WQMControlInterface:

    def __init__(self,serial_port,baud_rate):
        self.device = serial_port
        self.baud = baud_rate
        self.data_dir = "D:\\data\\wqm" # Change this directory
        self.datalogger = Logger("WQM Logger",self.data_dir,"wqm")
        print(f"[+] Initialized WQM Control Interface")


    def log_data(self):
        entry = self.read_wqm()
        if entry:
            self.datalogger.log.info(entry)

    def run(self):
        self.log_data()


    def send_command(self,cmd):
        with serial.Serial(port=self.device,baudrate=self.baud,timeout=0.5) as wqm:
            wqm.write(bytes(cmd,"utf-8"))
        print(f"[+] Sent Command:\t{cmd}")

  # Read serial output received from WQM
    def read_wqm(self):
         with serial.Serial(port=self.device,baudrate=self.baud,timeout=0.1) as wqm:

                data = wqm.readline().decode("utf-8")
                if data:
                  print(data)
                  return data

  # Stop sampling and enter standby mode
    def stop_wqm(self):
        self.send_command(f"!!!!")

    def start_wqm(self):
        self.send_command(f"$RUN\n\r")

    # Commands for configuring and controlling the bleach injection system
    def blis_display_setup(self):
        self.send_command(f"$BLD\n\r")

    def blis_set_non_pumped(self,pump_interval,no_static_squirts):
        self.send_command(f"$BLH {pump_interval} {no_static_squirts}\n\r")

    def blis_cycle_pump(self,no_cycles):
        self.send_command(f"$BLS {no_cycles}\n\r")

    def blis_reset_volume(self):
        self.send_command(f"$BLV 9999\n\r")

    def blis_purge(self,no_squirts):
        self.send_command(f"$PUR {no_squirts}\n\r")

    def blis_run_pump(self,speed,squirt_delay):
        self.send_command(f"$RPB {speed} {squirt_delay}\n\r")

    def blis_set_pumped(self,speed,squirts_delay):
        self.send_command(f"$SPB {speed} {squirts_delay}\n\r")



  # Control and sample commands

    def set_sample_mode(self,mode):
        self.send_command(f"$MDE {mode}\n\r")

    def set_sample_interval(self,HHMMSS):
        self.send_command(f"$INT {HHMMSS}\n\r")

    def set_sample_packet_size(self,pkt_size):
        self.send_command(f"$PKT {pkt_size}\n\r")

    def set_sample_delay(self,delay):
        self.send_command(f"$SSD {delay}\n\r")

    def set_do_stability(self,stability_time):
        self.send_command(f"$SPT {stability_time}\n\r")


    def set_startup_delay(self,delay):
        self.send_command(f"$SUD {delay}\n\r")


  # Ctd Commands
    def power_ctd(self):
        self.send_command(f"$CTD\n\r")

    def set_ctd_pump(self,speed):
        self.send_command(f"$RCP {speed}\n\r")

    def reset_ctd_pressure_offset(self):
        self.send_command(f"$RPO\n\r")


  # ECO commands
    def power_on_eco(self):
        self.send_command(f"$ECO\n\r")

    def power_off_eco(self):
        self.send_command(f"**********")
    def get_eco_calibration(self):
        self.send_command(f"$CHL\n\r")

    def set_eco_calibration(self,scale_factor,offset):
        self.send_command(f"$CHL {scale_factor} {offset}\n\r")

    def set_eco_shutter(self,state):
        self.send_command(f"$MVS {state}\n\r")


  # External Data Port Commands
    def set_edp(self,serial_no,scale_factor,offset):
        self.send_command(f"$CDOM {serial_no} {scale_factor} {offset}\n\r")

    def clear_edp(self):
        self.send_command(f"$CEDP 9999\n\r")

    def power_edp(self):
        self.send_command(f"$EDP\n\r")

    def get_edp_setup(self):
        self.send_command(f"$GEDP\n\r")

    def set_edp_par(self,serial_no, imm_coeff,a0,a1):
        self.send_command(f"$PAR {serial_no} {imm_coeff} {a0} {a1}\n\r")


  # File Handling Commands
    def get_raw_file_dir(self):
        self.send_command(f"$DIR\n\r")

    def erase_file(self,file):
        self.send_command(f"$EFN {file} {file}\n\r")

    def erase_memory_card(self):
        self.send_command(f"$EMC 8888\n\r")
#       self.send_command(f"$EMC 9999\n\r")
    def get_file(self,file):
        self.send_command(f"$GET {file}\n\r")

    def get_recent(self):
        self.send_command(f"$GRF\n\r")

    def increment_run_no(self):
        self.send_command(f"$IRN\n\r")

    def set_internal_logging(self,state):
        self.send_command(f"$REC {state}\n\r")


  # Misc Commands
    def set_baud(self,baud_rate):
        self.send_command(f"$BAU {baud_rate}\n\r")

    def get_help(self):
        self.send_command(f"$HLP\n\r")

    def test_comms(self,baud_rate,timeout):
        self.send_command(f"$TBR {baud_rate} {timeout}\n\r")

    def clear_ups_history(self):
        self.send_command(f"$UPS 9999\n\r")

    def exit_to_picodos(self):
        self.send_command(f"$XIT\n\r")


  # Output Commands
    def get_last_samples(self,no_samples):
        self.send_command(f"$GLXS {no_samples}\n\r")
    def set_data_output(self,state):
        self.send_command(f"$SDO {state}\n\r")

    def set_output_bits(self,output_bits):
        self.send_command(f"$SOB {output_bits}\n\r")

  # Status Commands
    def set_system_time(self,HHMMSS):
        self.send_command(f"$CLK\n\r")
        self.send_command(f"$CLK {HHMMSS}\n\r")

    def set_system_date(self,MMDDYY):
        self.send_command(f"$DAT\n\r")
        self.send_command(f"$DAT {MMDDYY}\n\r")

    def set_debug_msgs(self,state):
        self.send_command(f"$DBUG {state}\n\r")

    def get_status(self):
        self.send_command(f"$MNU\n\r")

    def set_status(self,state):
        self.send_command(f"$MNU {state}\n\r")

    def set_verbosity(self,state):
        self.send_command(f"$VER {state}\n\r")

if __name__ == '__main__':

    device = "COM1" # Change this
    baud = 19200
    ctd_control = WQMControlInterface(device,baud)

    while True:
        ctd_control.run()

