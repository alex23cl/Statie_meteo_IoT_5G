import firebase_admin
from firebase_admin import credentials, firestore
import bluetooth
import datetime
import select

# === init Firebase ===
cred = credentials.Certificate("weather-e95f2-firebase-adminsdk-fbsvc-d10785bb38.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# === MAC ESP32 ===
esp32_1_mac = 'B4:E6:2D:E8:C8:43'
esp32_2_mac = 'B4:E6:2D:E8:C3:0F'

# === conectare bluetooth ===
sock1 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock1.connect((esp32_1_mac, 1))
sock1.setblocking(False)

sock2 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock2.connect((esp32_2_mac, 1))
sock2.setblocking(False)

print("✅ Conectat la ambele ESP32")

# === bucla principala ===
while True:
    try:
        data1 = None
        data2 = None

        # check ESP32_1
        ready1, _, _ = select.select([sock1], [], [], 5)
        if ready1:
            try:
                data1 = sock1.recv(1024).decode().strip()
            except:
                data1 = None

        # check ESP32_2
        ready2, _, _ = select.select([sock2], [], [], 5)
        if ready2:
            try:
                data2 = sock2.recv(1024).decode().strip()
            except:
                data2 = None

        # payload
        payload = {
            "timestamp": datetime.datetime.now()
        }
        if data1:
            payload["esp32_1"] = data1
        if data2:
            payload["esp32_2"] = data2

        # update Firestore
        db.collection("weather_data").document("live").set(payload, merge=True)

        print(f"[OK] data1={data1} | data2={data2}")

    except Exception as e:
        print(f"[ERR] {e}")
