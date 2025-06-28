# Configurare senzori meteo - ESP32

Senzorii meteo trebuie să fie conectați corect la microcontrolerele ESP32 astfel:

## ESP32_1

- **Senzor BME280** (interfață I2C):
  - SCL (Serial Clock): conectat la pinul 22 al ESP32
  - SDA (Serial Data): conectat la pinul 21 al ESP32
  - Alimentare: 3.3V de pe ESP32
  - Masă: GND de pe ESP32

- **Senzor SI1145** (interfață I2C):
  - SCL (Serial Clock): conectat la pinul 22 al ESP32
  - SDA (Serial Data): conectat la pinul 21 al ESP32
  - Alimentare: 3.3V de pe ESP32
  - Masă: GND de pe ESP32

- **Senzor YL-83**:
  - Ieșire analogică: conectată la pinul ADC 36 al ESP32
  - Alimentare: 3.3V de pe ESP32
  - Masă: GND de pe ESP32

## ESP32_2

- **Giruetă**:
  - Ieșire analogică: conectată la pinul ADC 34 al ESP32

- **Anemometru**:
  - Ieșire digitală: conectată la pinul 22 al ESP32, configurat ca intrare cu întrerupere

- **Pluviometru**:
  - Ieșire digitală: conectată la pinul 33 al ESP32, configurat ca intrare cu întrerupere

