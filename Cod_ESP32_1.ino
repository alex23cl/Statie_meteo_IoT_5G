#include <BME280I2C.h>
#include "Adafruit_SI1145.h"
#include <Wire.h>
#include "BluetoothSerial.h"

// HL-83 + LED
const int analogPin = 36;
const int redLED = 15;
const int greenLED = 25;
int sensorValue = 0;
int thresholdValue = 4095;
bool raining = false;

// senzori BME + UV
#define SERIAL_BAUD 115200
BME280I2C bme;
Adafruit_SI1145 uv = Adafruit_SI1145();

BluetoothSerial SerialBT;

void setup() {
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  Serial.begin(SERIAL_BAUD);
  Wire.begin();

  SerialBT.begin("ESP32_1");

  while (!bme.begin()) delay(1000);
  if (!uv.begin()) while (1);

  Serial.println("ESP32_1 initializat");
}

void loop() {
  // senzor ploaie
  sensorValue = analogRead(analogPin);
  raining = sensorValue < thresholdValue;
  digitalWrite(greenLED, raining ? LOW : HIGH);
  digitalWrite(redLED, raining ? HIGH : LOW);

  // bme280
  float temp(NAN), hum(NAN), pres(NAN);
  bme.read(pres, temp, hum, BME280::TempUnit_Celsius, BME280::PresUnit_Pa);

  // UV
  int visible = uv.readVisible();
  int ir = uv.readIR();
  float uvIndex = uv.readUV() / 100.0;

  // date
  String weatherData = String("Rain: ") + (raining ? "Yes" : "No") + 
                       " | T: " + String(temp, 1) + "C" + 
                       " | H: " + String(hum, 1) + "%" +
                       " | P: " + String(pres, 1) + "Pa" +
                       " | V: " + visible +
                       " | IR: " + ir + 
                       " | UV: " + String(uvIndex, 1);

  // trimitem la fiecare minut
  static unsigned long lastSend = 0;
  unsigned long now = millis();
  if (now - lastSend > 60000) {  // 1 min
    Serial.println(weatherData);
    SerialBT.println(weatherData);
    lastSend = now;
  }

  delay(500); // bucla rapida
}