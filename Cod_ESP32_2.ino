#include "BluetoothSerial.h"

#define RAIN_PIN 33
#define WIND_DIR_PIN 34
#define ANEMOMETER_PIN 22
#define DEBOUNCE_TIME 15

BluetoothSerial SerialBT2;

unsigned long nextSend;
unsigned long timer;

volatile unsigned int rainTrigger = 0;
volatile unsigned long last_micros_rg;

volatile int anemometerCounter = 0;
volatile unsigned long last_micros_an;

float dirDeg[] = {90, 135, 180, 45, 225, 0, 315, 270};
char* dirCard[] = {"E", "SE", "S", "NE", "SW", "N", "NW", "W"};

int sensorMin[] = {350, 700, 1100, 1800, 2500, 3200, 3600, 3800};
int sensorMax[] = {450, 900, 1300, 2000, 2700, 3300, 3700, 4000};

void countingRain() {
  if ((long)(micros() - last_micros_rg) >= DEBOUNCE_TIME * 1000) {
    rainTrigger += 1;
    last_micros_rg = micros();
  }
}

void countAnemometer() {
  if ((long)(micros() - last_micros_an) >= DEBOUNCE_TIME * 1000) {
    anemometerCounter++;
    last_micros_an = micros();
  }
}

float convertToRainVolume(unsigned int tips) {
  float volumePerTip = 0.1;
  return tips * volumePerTip * 25;
}

int readWindSpd() {
  long spd = 14920;
  spd *= anemometerCounter;
  spd /= 10000;
  anemometerCounter = 0;
  return (int) spd;
}

String getWindDirection() {
  int incoming = analogRead(WIND_DIR_PIN);
  int closestIndex = 0;
  int closestDiff = abs(incoming - (sensorMin[0] + sensorMax[0]) / 2);
  for (int i = 1; i < 8; i++) {
    int currentDiff = abs(incoming - (sensorMin[i] + sensorMax[i]) / 2);
    if (currentDiff < closestDiff) {
      closestDiff = currentDiff;
      closestIndex = i;
    }
  }
  return dirCard[closestIndex];
}

void setup() {
  Serial.begin(9600);
  SerialBT2.begin("ESP32_2");
  Serial.println("ESP32_2 Bluetooth Started");
  SerialBT2.println("ESP32_2 Bluetooth Started");

  pinMode(RAIN_PIN, INPUT);
  pinMode(ANEMOMETER_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), countingRain, RISING);
  attachInterrupt(digitalPinToInterrupt(ANEMOMETER_PIN), countAnemometer, FALLING);

  nextSend = millis() + 60000;  // 1 minut
}

void loop() {
  timer = millis();
  if (timer > nextSend) {
    nextSend = timer + 60000;  // 1 minut

    float estimatedRainVolume = convertToRainVolume(rainTrigger);
    int windSpeed = readWindSpd();
    String windDirection = getWindDirection();

    String weatherData = String("Rain Vol: ") + estimatedRainVolume +
                         " | Wind Speed: " + windSpeed +
                         " km/h | Wind Dir: " + windDirection;

    Serial.println(weatherData);
    SerialBT2.println(weatherData);

    rainTrigger = 0; // resetam la fiecare minut
  }
}