#include "LowPower.h"

int SIG_LED = 2;
int WIFI_SIG = 3;
int Pi_on = 5;
int IO = 6;
int Sampling_LED = 7;
int STROBE = 9;


int RECOVER = 0;
int Extend_Sleep = 0;
int SAMPLES = 0;
int MAX_Sample_Num = 3000;


void setup(void)
{
  pinMode(SIG_LED, OUTPUT);
  pinMode(WIFI_SIG, INPUT_PULLUP);
  pinMode(IO, INPUT_PULLUP);
  pinMode(Pi_on, OUTPUT); 
  pinMode(Sampling_LED, OUTPUT);
  pinMode(STROBE, OUTPUT);

  digitalWrite(SIG_LED, LOW);
  digitalWrite(Pi_on, LOW);
  digitalWrite(Sampling_LED, LOW);
  digitalWrite(STROBE, LOW);

  for(int i = 0; i < 3; i++){
    digitalWrite(Sampling_LED, HIGH);
    digitalWrite(SIG_LED, HIGH);
    delay(400);
    digitalWrite(Sampling_LED, LOW);
    digitalWrite(SIG_LED, LOW);
    delay(100);
  }
}

void Pi_Samp() {
  digitalWrite(Pi_on, HIGH);

  for (int i = 1; i <= 12; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  int WIFI_Status = digitalRead(WIFI_SIG);
  int Mission_Status = digitalRead(IO);

  do {
    digitalWrite(Sampling_LED, HIGH);
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
    WIFI_Status = digitalRead(WIFI_SIG);
    Mission_Status = digitalRead(IO);
    if (Mission_Status == LOW){
      RECOVER = 1;
    }
  }
  while (WIFI_Status == HIGH);

  digitalWrite(Sampling_LED, LOW);

  for (int i = 1; i <= 5; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  digitalWrite(Pi_on, LOW);
}

void Pi_Samp_RECOVER() {

  digitalWrite(Pi_on, HIGH);

  for (int i = 1; i <= 12; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  int WIFI_Status = digitalRead(WIFI_SIG);
  int Mission_Status = digitalRead(IO);

  do {
    digitalWrite(Sampling_LED, HIGH);
    strobe();
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
    WIFI_Status = digitalRead(WIFI_SIG);
    Mission_Status = digitalRead(IO);
    if (Mission_Status == LOW){
      Extend_Sleep = 1;
    }
  }
  while (WIFI_Status == HIGH);

  digitalWrite(Sampling_LED, LOW);

  for (int i = 1; i <= 5; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  digitalWrite(Pi_on, LOW);
}


void strobe() {
  digitalWrite(STROBE, HIGH);
  delay(100);
  digitalWrite(STROBE, LOW);
  delay(400);

  digitalWrite(STROBE, HIGH);
  delay(250);
  digitalWrite(STROBE, LOW);
  delay(750);

  digitalWrite(STROBE, HIGH);
  delay(100);
  digitalWrite(STROBE, LOW);
  delay(400);
}

void loop(void) 
{

  Pi_Samp();

  SAMPLES = SAMPLES + 1;

  if (RECOVER == 1 || SAMPLES > MAX_Sample_Num) {

    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
    RECOVER = 0;

    while(1) {
      Pi_Samp_RECOVER();

      //This is the sleep cycle! Set for 180 cycles of 10 seconds for 30 minutes
      for (int i = 1; i <= 180; i++){
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
        strobe();
      }

      if (Extend_Sleep == 1){
        //This is the sleep cycle! Set for 180 cycles of 10 seconds for 30 MORE minutes asleep
        for (int i = 1; i <= 180; i++){
          LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
          strobe();
        }
      }
    }
  }
  //This is the sleep cycle! Set for 300 cycles of 4 seconds for 20 minutes
  for (int i = 1; i <= 300; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

}








