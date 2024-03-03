#ifndef CORE_PMA_H
#define CORE_PMA_H
#include <Arduino.h>
#include "profet_pmm.h"

/* Class definition of CorePMA for L4 Buoy Power Management Array
 * CorePMA utilizes the ProfetPMM class module to create interfaces
 * to Infineon Profet hardware
 */

/* A PROFET module connected directly to an arduino has the following pin configuration
 * > Battery Voltage Sense: A1
 * > CH 1: Trigger Pin D9;  Is Pin A2; DEN Pin D6
 * > CH 2: Trigger Pin D10; Is Pin A2; DEN Pin D8
 * > CH 3: Trigger Pin D11; Is Pin A3; DEN Pin D6
 * > CH 4: Trigger Pin D3;  Is Pin A3; DEN Pin D8
*/
const int N_OF_MODULES = 1;
const int N_OF_CHANNELS = 4;
const int M1_P_CH_1[4] = {4,9,2,6};
const int M1_P_CH_2[4] = {5,10,2,8};
const int M1_P_CH_3[4] = {12,11,3,6};
const int M1_P_CH_4[4] = {13,3,3,8};

class CorePMA {

  public:
      // ProfetPMM imcs_pmm_1[4] = { ProfetPMM(1,1, ...), ... };
      // ProfetPMM imcs_pmm_2[4] = { ProfetPMM(2,1, ...), ... };
      ProfetPMM imcs_channels[N_OF_CHANNELS] = {
      ProfetPMM(1,1,M1_P_CH_1[0],M1_P_CH_1[1],M1_P_CH_1[2],1,M1_P_CH_1[3]),
      ProfetPMM(1,2,M1_P_CH_2[0],M1_P_CH_2[1],M1_P_CH_2[2],1,M1_P_CH_2[3]),
      ProfetPMM(1,3,M1_P_CH_3[0],M1_P_CH_3[1],M1_P_CH_3[2],1,M1_P_CH_3[3]),
      ProfetPMM(1,4,M1_P_CH_4[0],M1_P_CH_4[1],M1_P_CH_4[2],1,M1_P_CH_4[3]),
    };

    CorePMA();
    void init();
    void run(); 
    String core_status(bool verbose);
    void set_power_ch(int channel,bool state);
    void cycle_power_ch(int channel);


};


#endif
