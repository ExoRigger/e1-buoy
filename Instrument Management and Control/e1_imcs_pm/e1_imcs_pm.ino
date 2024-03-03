
#include "core_pma.h"

#define PAR_SENSOR_PIN 7

CorePMA imcs_core;

/* MCU Initialization
 * Binds a UART link via USB and an auxiliary serial port at 9600b
 * Invokes the initializer function for the core system 
 */
void setup() {
  analogReadResolution(12u);
  SerialASC.begin(9600);
  Serial1.begin(9600);
  imcs_core.init();
  
  while ((!SerialASC) || (!Serial1)) {
    ; // wait
  }

  if (SerialASC) {
    SerialASC.println("[+] Core System Initialized");
    SerialASC.println("[x] Primary Link Ready");
    PrintBanner(SerialASC,false);
  
  }
  else if (Serial1) {
    Serial1.println("[+] Core System Initialized");
    Serial1.println("[x] Override Link Ready");
    PrintBanner(Serial1,false);
  }
}

/* Control loop
 *  System is programmed to be polled over SerialASC (USB) and Serial1
 *  We listen for activity over SerialASC and Serial1
 *  Input commands are parsed and return 'OK' upon success.
 *  Unregistered inputs are dropped
 *  TODO: Add error code table (e.g. 'invalid command', 'failed to execute')
 */
void loop() {
  
  if (SerialASC.available()) {
    ParseCmd(SerialASC);
}
  else if (Serial1.available()) {
    ParseCmd(Serial1);
}
  imcs_core.run();
  
}

/* Initialization and help banner
 * Displays an initialization banner and optionally the list of valid commands
 * Inputs: 
 *   > Stream &serial_port
 *   > bool help - Set to display list of commands, clear to display only the banner
 */
void PrintBanner(Stream &serial_port,bool help) { 
    if (!help) {
      serial_port.println("+--------------------------------------------------------------+");
      serial_port.println("|      - E1 Buoy Instrument Management and Control v2.0 -      |");
      serial_port.println("+--------------------------------------------------------------+");
      
      serial_port.println("|        ***        Enter 'h' for commands         ***         |");
    }
    else {
      serial_port.println("---------------------------------------------------------------+");
      serial_port.println("|           ***           COMMANDS           ***               |");
      serial_port.println("---------------------------------------------------------------+");
      serial_port.println("| * 'h' - Display this help text                             * |");
      serial_port.println("| * 'v' - Display PMM status information (Human Readable)    * |");
      serial_port.println("| * 'i' - Display PMM status information                     * |");
      serial_port.println("| * 'c <int channel>' - Cycle power channel                  * |");  
      serial_port.println("| * 't <int channel>' - Toggle power channel state           * |");
      serial_port.println("| * 's <int channel>' <bool state> - Set power channel state * |"); 
    }
      serial_port.println("+--------------------------------------------------------------+\n");
}

/* Sanitize and process input data from Serial peripherals
 *  Commands are input as a single character and any parameters
 *  are separated by a space. Commands are terminated by a newline.
 *  Commands registered by the system:
 * 'c <int channel>' - Power cycle a PMM channel given as an integer. 
 * 's <int channel> <bool state>' - Set a PMM channel given as an integer to a boolean state 
 * 'i' - Return a compressed data string of all PMM voltages, PMM channel states and current draw
 * 'v' - Returns a verbose data string of all PMM voltages, PMM channel states and current draw
 * TODO: add 't' - function test option and 'h' - help option 
 */
void ParseCmd(Stream &serial_port) {

  char cmd = serial_port.read();

  // Power cycle a channel
  if (cmd == 'c') {
    int ch = serial_port.parseInt();
    serial_port.print("[+] CYCLE ");
    serial_port.print(ch);
    imcs_core.cycle_power_ch(ch);
    serial_port.println("[+] OK"); 
  }

  else if (cmd == 'h') {
    PrintBanner(serial_port,true);
    serial_port.println("[+] OK"); 
  }
  
  // Set channel state (true: channel on, false: channel off)
  else if (cmd == 's') {
    int ch = serial_port.parseInt();
    int state = serial_port.parseInt();
    serial_port.print("[+] SET ");
    serial_port.print(ch);
    serial_port.print(" | ");
    serial_port.print(state);
    
    imcs_core.set_power_ch(ch,state);
    serial_port.println("[+] OK"); 
  }

  // Display system info (condensed)
  else if (cmd == 'i') {
    serial_port.println(imcs_core.core_status(false)); 
    serial_port.println("[+] OK"); 
  }
  // Display system info (human-readable)
    else if (cmd == 'v') {
    serial_port.println(imcs_core.core_status(true)); 
    serial_port.println("[+] OK"); 
  }
  // Sample analog pin connected to PAR sensor and return voltage
    else if (cmd == 'p') {
      serial_port.println(analogRead(PAR_SENSOR_PIN)*(5.0/1023.0));
      serial_port.println("[+] OK"); 
    }
  }
