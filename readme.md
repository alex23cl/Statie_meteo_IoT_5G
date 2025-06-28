# Stație Meteo IoT 5G

Acest proiect reprezintă o stație meteo inteligentă, capabilă să colecteze și să transmită în timp real parametrii meteorologici folosind tehnologii IoT (ESP32, Raspberry Pi) și conectivitate 5G prin modemul Fibocom EVB M2. Datele sunt salvate într-un backend Firebase și afișate printr-o interfață web dezvoltată cu NiceGUI.

---

Structură repository:

- `/Cod_ESP32_1/` → cod sursă pentru ESP32_1 (achiziție temperatură, presiune, umiditate, UV, lumină, ploaie)
- `/Cod_ESP32_1/` → cod sursă pentru ESP32_2 (viteză vânt, direcție vânt, volum precipitații)
- `/Cod_raspberry/` → script Python pentru agregarea și transmiterea datelor către Firebase
- `/app.py/` → aplicația web (NiceGUI) pentru afișare date
- `/sensor_config/` → documentație tehnică (schema hardware, arhitectură sistem)
- `README.md` → acest fișier

---

## Pași de compilare

### Compilare ESP32

1. Descarcă și instalează Arduino IDE
2. Configurează placa: **Sparkfun Thing Plus ESP32**
3. Instalează librăriile:
   - Adafruit_SI1145
   - BME280I2C
   - BluetoothSerial
   - Wire (implicit în IDE)
4. Deschide:
   - `Cod_ESP32_1.ino` → încarcă pe ESP32_1
   - `Cod_ESP32_2.ino` → încarcă pe ESP32_2

---

### Compilare Raspberry Pi

1. Instalează Python 3 (>= 3.9)
2. Instalează dependințele:
   ```bash
   pip install firebase-admin pybluez
   ```
3. Rulează scriptul:
   ```bash
   python Cod_raspberry.py
   ```
   > Asigură-te că fișierul de autentificare Firebase (`weather-e95f2-firebase-adminsdk.json`) este prezent în directorul scriptului.

---

### Configurare Firebase

1. Creazǎ un proiect Firestore.
2. Descarcă cheia JSON de serviciu și salveaz-o ca (`weather-e95f2-firebase-adminsdk.json`).
3. Configurează regulile Firestore pentru acces în siguranță.
4. În consola Firebase, creează colecția weather_data cu documentul live pentru datele în timp real.

---

### Compilare aplicație NiceGUI

1. Instalează dependințele:
   ```bash
   pip install nicegui firebase-admin pandas
   ```
2. Rulează aplicația:
   ```bash
   python app.py
   ```
3. Accesează aplicația în browser pe `http://localhost:8080`

---

## Pași de instalare și lansare

- Conectează toți senzorii la cele două ESP32-uri conform schemei din `/sensor_config/`
- Încarcă firmware-ul pe ambele plăci
- Configurează modemul Fibocom EVB M2 pentru conectivitate 5G pe Raspberry Pi
- Rulează scriptul de colectare date pe Raspberry Pi
- Configureazǎ proiectul Firestore
- Rulează aplicația NiceGUI
- Accesează aplicația web și vizualizează datele live

---

## Livrabile proiect

- codul sursă complet ESP32 (Arduino)
- codul sursă Raspberry Pi (Python)
- aplicația web (NiceGUI)
- configurarea senzorilor 
- fișierul de configurare Firebase (exclus din repo public)
- README.md (acest fișier)

---

## Suport

**Autor:** Goleșie Alex-Claudiu
**Coordonator:** Prof. dr. ing. Vasile Stoicu-Tivadar
**Universitatea Politehnica Timișoara — Facultatea de Automatică și Calculatoare**

