#include "LowPower.h"

int WIFI_SIG = 3;
int Pi_on = 5;
int IO = 6;
int Sampling_LED = 7;
int STROBE = 9;


int RECOVER = 0;
int Extend_Sleep = 0;
int SAMPLES = 0;
int MAX_Sample_Num = 3000;


void soft_pwm(void)
{
  analogWrite(STROBE, 100);
  delay(200);
  digitalWrite(STROBE, LOW);
  delay(100);
}

void hard_pwm(void)
{
  for (int j = 1; j <= 2; j++) {

    analogWrite(STROBE, 200);
    delay(200);
    digitalWrite(STROBE, LOW);
    delay(100);

  }
}

void setup(void)
{
  pinMode(WIFI_SIG, INPUT_PULLUP);
  pinMode(IO, INPUT_PULLUP);
  pinMode(Pi_on, OUTPUT); 
  pinMode(Sampling_LED, OUTPUT);
  pinMode(STROBE, OUTPUT);

  digitalWrite(Pi_on, LOW);
  digitalWrite(Sampling_LED, LOW);
  digitalWrite(STROBE, LOW);


  for (int jj = 1; jj <= 3; jj++) {
    digitalWrite(Sampling_LED, HIGH);
    soft_pwm();
    digitalWrite(Sampling_LED, LOW);
    delay(300);
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
    hard_pwm();
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
        hard_pwm();
      }

      if (Extend_Sleep == 1){
        //This is the sleep cycle! Set for 180 cycles of 10 seconds for 30 MORE minutes asleep
        for (int i = 1; i <= 180; i++){
          LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
          hard_pwm();
        }
      }
    }
  }
  //This is the sleep cycle! Set for 225 cycles of 4 seconds for 15 minutes
  for (int i = 1; i <= 225; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

}











