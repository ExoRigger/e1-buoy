#include "core_pma.h"


/* Class implementation of CorePMA for L4 Buoy Power Management Array
 *  Functions:
 *  init() - Initializer function for configuring power channels
 *  run() - Update memory with most recent power channel measurements
 *  core_status(verbose) - Return an optionally verbose string of instantaneous power channel activity
 *  set_power_ch(int channel, bool state) - Set a power channel on/off
 *  cycle_power_ch(int ch, int duration) - Clears a power channel for <duration> seconds, then sets the channel
 * 
 */



CorePMA::CorePMA() {
  init();
}

// Initialize Power Core
void CorePMA::init() {
; // Initialize IMCS Power Channels
  this->imcs_channels[N_OF_CHANNELS] = imcs_channels[N_OF_CHANNELS];
  setMode(0); // 0 - Polling mode, 1 - streaming mode
}


void CorePMA::setMode(int mode) {
  this->MODE = mode;
}

// Temporally Evolve Power Core
void CorePMA::run() {
  ; // Update state by reading I/Os 
    for (int i=0;i<N_OF_CHANNELS;i++) {
    String info = this->imcs_channels[i].read_ch(false);
    }
}

String CorePMA::core_status(bool verbose) {
  String status_string = "";
  if (verbose) {
  status_string += "+--------------------------------------------------------------+\n";
  status_string += "|          ***          IMC CORE STATUS:          ***          |\n";
  status_string += "+--------------------------------------------------------------+\n";

  status_string += "                        V_bat: ";
  float v = float(5.7 * (analogRead(1)*(5.0/4095.0)));
  status_string += String(v);
  status_string += "V\n";

  status_string += "+--------------------------------------------------------------+\n";
  ; // Grab status from each power channel  
  for (int i=0;i<N_OF_CHANNELS;i++) {
      status_string += this->imcs_channels[i].read_ch(true);
    }
  }

  else {
      for (int i=0;i<N_OF_CHANNELS;i++) {
         status_string += this->imcs_channels[i].read_ch(false);
    }
    
  }
  //status_string += "+--------------------------------------------------------------+\n";
  return status_string;
}

// Make a separate function to pull input channel from array
void CorePMA::set_power_ch(int channel,bool state) {
  for (int i=0;i<N_OF_CHANNELS;i++) {
    if (channel == this->imcs_channels[i].channel_no) {
      this->imcs_channels[i].set_ch(state);
    }
    else {
      continue;
    }
}
}

void CorePMA::cycle_power_ch(int channel) {
  for (int i=0;i<N_OF_CHANNELS;i++) {
    if (channel == this->imcs_channels[i].channel_no) {
      this->imcs_channels[i].cycle_ch(5);
    }
    else {
      continue;
    }

}
}

void CorePMA::toggle_power_ch(int channel) {
  for (int i=0;i<N_OF_CHANNELS;i++) {
    if (channel == this->imcs_channels[i].channel_no) {
      this->imcs_channels[i].toggle_ch();
    }
}
}
