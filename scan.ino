#include <ELECHOUSE_CC1101_SRC_DRV.h>

#define CC1101_CS 5

float startFreq = 430.0;
float endFreq = 440.0;
float stepFreq = 0.1;

void setup() {
  Serial.begin(115200);

  ELECHOUSE_cc1101.setSpiPin(18, 19, 23, CC1101_CS);
  ELECHOUSE_cc1101.Init();

  ELECHOUSE_cc1101.SetRx();
}

void loop() {

for(float freq = startFreq; freq <= endFreq; freq += stepFreq){

    ELECHOUSE_cc1101.setMHZ(freq);
    delay(5);

    int rssi = ELECHOUSE_cc1101.getRssi();

    Serial.print(freq);
    Serial.print(":");
    Serial.print(rssi);

    if(freq < endFreq) Serial.print(",");
}
Serial.println();
}