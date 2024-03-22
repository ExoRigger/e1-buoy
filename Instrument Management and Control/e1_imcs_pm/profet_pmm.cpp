#include "profet_pmm.h"

/* Class implementation of Infineon PROFET Power Management Module Interface
 * Each module consists of 4 high-side switches with digital inputs IN1,IN2,IN3,IN4
 * A pair of inputs (IN1 + IN3) have an analog Isense pin which can be read for information about the load status
 * This requires use of the DEN pins to toggle diagnostics mode for a pair of switches - IN1 + IN3 are coupled to one pin, as are IN2 + IN4.
 * Optional external resistors can be connected for enhanced functionality (e.g. open/short circuit detection, partial load loss detection)
 * 
 * Class implementation currently considers a single channel attached to an indexed module
 * TODO: Group channels into 4 as per module spec
 * TODO: Add 'test_module()' 
 * 
*/

/* PMM Constructor
 *  Initializes a PMM channel object and binds to hardware
 *  Inputs:
 *    <int module_no>
 *    <int channel_no>
 *    <int switch_pin>
 *    <int isense_pin>
 *    <int den1_pin>
 *    <int den2_pin>
 */
ProfetPMM::ProfetPMM(int module_no, int channel_no,int led_pin, int switch_pin, int sense_pin, int v_bat, int den_pin) {
  this->module_no = module_no; // replace with pmm struct with all the data, creating a channel object will require a struct
  this->v_bat = v_bat;
  this->channel_no = channel_no;
  this->led_pin = led_pin;
  this->switch_pin = switch_pin;
  this->sense_pin = sense_pin;
  this->den_pin = den_pin;
  this->state = 1;
  this->current = 0;
  init();
}

/* Further Initialization, called during void Setup() in e1_imcs_pm.ino
 * Set DEN pins to low state
 * Set all output channels to low state
 * 
 */
void ProfetPMM::init() {
  pinMode(this->led_pin, OUTPUT);
  pinMode(this->switch_pin, OUTPUT);
  pinMode(this->den_pin,OUTPUT);
  digitalWrite(den_pin,LOW);
  set_ch(true);
  read_ch();
}

/* 
 * Generate status string for power channel instance
 * Inputs: 
 *   <bool verbose> - Set for human readable output, clear for computer parsable format
 *   
 * Returns:
 *   <String status_string> - A string containing voltages and currents 
 */
String ProfetPMM::status(bool verbose) {
  // Generate Status String for power channel instance
  String status_string = "";
  digitalWrite(this->den_pin,HIGH);
  delay(20);
  if (verbose) {
      status_string += "    PMM: ";
      status_string += String(this->module_no);
      status_string += " | CH: ";
      status_string += String(this->channel_no);
      status_string += " | ";
      status_string += "Output: ";
      status_string += String(this->state);
      status_string += " | ";
      status_string += "Vs: ";
      status_string += String(analogRead(this->v_bat)*((5.0/4095.0)* 5.7));
      status_string += "V | ";
      status_string += "Current: ";
      status_string += String(analogRead(this->sense_pin)*(5.0/4095.0)); // Calculate current through another function or in a variable above
      status_string += "mA\n";
      status_string += "|--------------------------------------------------------------|\n";
  }
  else {
      status_string += String(this->module_no);
      status_string += ",";
      status_string += String(this->channel_no);
      status_string += ",";
      status_string += String(this->state);
      status_string += ",";
      status_string += String(analogRead(this->sense_pin)*(5.0/4095.0)); // Calculate current through another function or in a variable above
      status_string += ";\n";
  }
  
  digitalWrite(this->den_pin,LOW);
  
  return status_string;
}


/*
 * Read all PMM channel voltages and currents
 * This involves reading in pairs due to the coupling
 * of the DEN pins (i.e read ch 1,ch 3 then ch 2,ch 4
 */
void ProfetPMM::read_ch() {
  this->state = digitalRead(this->switch_pin);  
  //this->current = float(analogRead(this->sense_pin)*(5.0/4095.0));
  //this->v_bat = float(analogRead(this->v_bat)*(5.0/4095.0));
}

/*
 * Set PMM channel high / low
 * Inputs:
 *   <int ch>
 *   <bool state>
 */
void ProfetPMM::set_ch(bool state) {
  if (state) {
    digitalWrite(this->switch_pin, HIGH);
    digitalWrite(this->led_pin, HIGH);
  }
  else {
    digitalWrite(this->switch_pin, LOW);
    digitalWrite(this->led_pin, LOW);
  }
}

/* Performs a power cycle
 * 
 */
void ProfetPMM::cycle_ch(int duration) {
  set_ch(false); //digitalWrite(this->pin,LOW);
  delay(duration*1000); // Duration in sec
  set_ch(true); //digitalWrite(this->pin,HIGH); 

}

void ProfetPMM::toggle_ch() {
  bool state = digitalRead(this->switch_pin);
  digitalWrite(this->switch_pin,!state);
  digitalWrite(this->led_pin, !state);
}
