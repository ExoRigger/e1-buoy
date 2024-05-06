#include "core_pma.h"

#define PAR_SENSOR_PIN 7

CorePMA imcs_core;

enum COMMAND_OPTIONS {
  HELP = 'h',
  VERBOSE_INFO = 'v',
  INFO = 'i',
  MODE = 'm',
  CYCLE_CH = 'c',
  TOGGLE_CH = 't',
  SET_CH = 's',
  READ_PAR = 'p',
};

/* MCU Initialization
 * Binds a UART link via USB and an auxiliary serial port at 115200b
 * Sets ADC resolution to 12bit (10bit is default)
 * Invokes the initializer function for the core system 
 */
void setup() {
  analogReadResolution(12u);
  SerialASC.begin(115200);
  Serial0.begin(115200);
  imcs_core.init();
  
  while ((!SerialASC) || (!Serial0)) {
    ; // wait
  }

  if (SerialASC) {
    SerialASC.println("[+] Core System Initialized");
    SerialASC.println("[x] Primary Link Ready");
    PrintBanner(SerialASC,false);
  
  }
  if (Serial0) {
    Serial0.println("[+] Core System Initialized");
    Serial0.println("[x] Override Link Ready");
    PrintBanner(Serial0,false);
  }
}

/* Control loop
 *  System is programmed to be polled over SerialASC (USB) and Serial
 *  We listen for activity over SerialASC and Serial
 *  Input commands are parsed and return 'OK' upon success.
 *  Unregistered inputs are dropped
 */
void loop() {
  if (SerialASC.available() > 0) {
    ParseCmd(SerialASC);
}
  if (Serial0.available() > 0) {
    ParseCmd(Serial0);

}
  if (imcs_core.MODE == 1) {
      SerialASC.print(imcs_core.core_status(false));
      SerialASC.println(analogRead(PAR_SENSOR_PIN)*(5.0/4095.0));
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
      serial_port.println("| * 'm <int channel>'  - Set mode (0 = POLL, 1 = STREAM)     * |");
      serial_port.println("| * 'p  - Measure voltage channel from connected PAR         * |"); 
    }
      serial_port.println("+--------------------------------------------------------------+\n");
}


void handleHelp(Stream &serial_port) {
    serial_port.print("[O] HELP\n");
    PrintBanner(serial_port,true);
    serial_port.println("\n[+] OK"); 
  ;
}

void handleVinfo(Stream &serial_port) {
    serial_port.print("[O] VINFO\n");
    serial_port.println(imcs_core.core_status(true)); 
    serial_port.println("\n[+] OK"); 
}

void handleInfo(Stream &serial_port) {
    serial_port.print("[O] INFO\n");
    serial_port.println(imcs_core.core_status(false)); 
    serial_port.println("\n[+] OK"); 
}

void handleMode(Stream &serial_port) {
    serial_port.print("[O] SET MODE > ");
    int mode = serial_port.parseInt();
    serial_port.println(mode);
    imcs_core.setMode(mode);
    serial_port.println("\n[+] OK"); 
}

void handleCycle(Stream &serial_port) {
    serial_port.print("[O] CYCLE CH > ");
    int ch = serial_port.parseInt();
    serial_port.print(ch);
    imcs_core.cycle_power_ch(ch);
    serial_port.println("\n[+] OK");
  ;
}

void handleToggle(Stream &serial_port) {
  serial_port.print("[O] TOGGLE CH > ");
  int ch = serial_port.parseInt();
  serial_port.print(ch);
  imcs_core.toggle_power_ch(ch);
  serial_port.println("\n[+] OK"); 
}

void handleSet(Stream &serial_port) {
    serial_port.print("[O] SET CH > ");
    int ch = serial_port.parseInt();
    serial_port.print(ch);
    serial_port.print("\n[+] SET CH STATE > ");
    int state = serial_port.parseInt();
    serial_port.print("\n");
    serial_port.print(state);
    imcs_core.set_power_ch(ch,state);
    serial_port.println("\n[+] OK"); 
}

void handleReadPar(Stream &serial_port) { 
    serial_port.print("[O] READ_PAR: ");
    serial_port.println(analogRead(PAR_SENSOR_PIN)*(5.0/4095.0));
    serial_port.println("\n[+] OK"); 
}

/* Sanitize and process input data from Serial peripherals
 *  Commands are input as a single character and any parameters
 *  are separated by a space. Commands are terminated by a newline.
 *  Commands registered by the system:
 * 'c <int channel>' - Power cycle a PMM channel given as an integer. 
 * 's <int channel> <bool state>' - Set a PMM channel given as an integer to a boolean state 
 * 'i' - Return a compressed data string of all PMM voltages, PMM channel states and current draw
 * 'v' - Returns a verbose data string of all PMM voltages, PMM channel states and current draw 
 */
void ParseCmd(Stream &serial_port) {
  char cmd_buf;
  cmd_buf = serial_port.read();

  switch (cmd_buf) {
    case HELP:
      handleHelp(serial_port);
      break;
    case VERBOSE_INFO:
      handleVinfo(serial_port);
      break;
    case INFO:
      handleInfo(serial_port);
      break;
    case MODE:
      handleMode(serial_port);
      break;
    case CYCLE_CH:
      handleCycle(serial_port);
      break;
    case TOGGLE_CH:
      handleToggle(serial_port);
      break;
    case SET_CH:
      handleSet(serial_port);
      break;
    case READ_PAR:
      handleReadPar(serial_port);
      break;

    default:
      serial_port.println("[E1 IMC]$> ");
  }

}
