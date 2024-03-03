#ifndef PROFET_PMM_H
#define PROFET_PMM_H

/* Class definition of Infineon PROFET Power Management Module Interface
 * Each module consists of 4 high-side switches with digital inputs IN1,IN2,IN3,IN4
 * A pair of inputs (IN1 + IN3) have an analog Isense pin which can be read for information about the load status
 * This requires use of the DEN pins to toggle diagnostics mode for a pair of switches
*/
class ProfetPMM {
  
  public:
    int module_no; // Index the modules if many are installed
    int channel_no;  // Channel of the power management module
    int led_pin; // indicator led
    int switch_pin;  // 
    int sense_pin; // Isense pin for
    int v_bat;
    int den_pin; // Diagnosis pin for channels 1 + 3 or 2 + 4
    bool state; 
    float current;
    ProfetPMM(int module_no, int channel_no,int led_pin, int switch_pin, int sense_pin, int v_bat, int den_pin);

    // Standard diagnostics functions
    void init();
    String status(bool verbose);
    void read_ch();
    void set_ch(bool state);
    void cycle_ch(int duration);

    // Advanced diagnostics functions
    void diag_open_load(); // Open load detection
    void diag_short_gnd(); // Short to GND Detection
    void diag_short_bat(); // Short to battery Detection
    void diag_nominal_load(); // Nominal Load Detection
    void diag_load_loss(); // Partial Load Loss Detection
    void diag_overload(); // Overload Detection

} ;

#endif
