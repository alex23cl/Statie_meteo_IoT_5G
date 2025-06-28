from nicegui import ui
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import re
import pandas as pd
import tempfile

# === Firebase init ===
cred = credentials.Certificate("weather-e95f2-firebase-adminsdk-fbsvc-d10785bb38.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# === Google Fonts & CSS ===
ui.add_head_html("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Roboto', sans-serif; }
  .card {
    transition: transform 0.3s ease;
  }
  .card:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  }
  .clock {
    position: fixed;
    top: 16px;
    right: 16px;
    background: rgba(255,255,255,0.6);
    padding: 4px 8px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    font-size: 1rem;
  }
</style>
""")

def create_card(title, emoji, color, unit):
    with ui.card().classes('flex flex-col items-center justify-center rounded-xl p-4').style(
        f'''
        flex: 1;
        height: 100%;
        min-width: 0;
        background-color: {color};
        color: #000;
        border: 1px solid #ccc;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        '''
    ) as card:
        ui.label(emoji).classes('text-5xl mb-2')
        ui.label(title).classes('text-xl font-semibold mb-1')
        value_label = ui.label('---').classes('text-4xl font-bold')
        return value_label

# === UI ===
@ui.page('/')
def main():

    # header centrat garantat
    with ui.row().classes('w-full justify-center shadow-md p-4'):
        with ui.column().classes('items-center'):
            ui.image('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Weather_icon_-_sunny.svg/120px-Weather_icon_-_sunny.svg.png').classes('h-14')
            ui.label('🌤️ Stație Meteo 5G').classes('text-4xl font-extrabold text-gray-800 mt-2')
            ui.label('Monitorizare meteo în timp real prin 5G').classes('text-sm italic text-gray-600 mb-2')

    # ceas absolut

    def update_time():
        time_label.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ui.timer(1, update_time)

    # === Carduri
    temp_label = hum_label = pres_label = uv_label = light_label = ir_label = None
    wind_speed_label = wind_dir_label = rain_vol_label = None

    with ui.row().classes('w-full p-4 flex-wrap gap-4 justify-center'):
        temp_label = create_card('Temperatură', '🌡️', '#fde2e4', '°C')
        hum_label = create_card('Umiditate', '💧', '#d0f4de', '%')
        pres_label = create_card('Presiune', '🌪️', '#f9f9c5', 'hPa')

    with ui.row().classes('w-full p-4 flex-wrap gap-4 justify-center'):
        uv_label = create_card('UV Index', '☀️', '#ffe5b4', '')
        light_label = create_card('Lumina', '💡', '#d0e6fa', 'lux')
        ir_label = create_card('Infraroșu', '🌈', '#e2d5f8', 'mW/cm²')

    with ui.row().classes('w-full p-4 flex-wrap gap-4 justify-center'):
        wind_speed_label = create_card('Viteză vânt', '💨', '#f8d7da', 'km/h')
        wind_dir_label = create_card('Direcție vânt', '🧭', '#d1e7dd', '')
        rain_vol_label = create_card('Volum precipitații', '🌧️', '#cfe2f3', 'mm')

    # === Timestamp
    last_update_label = ui.label('Ultima actualizare: ---').classes('text-xs mt-2 italic')

    # === Export buton
    def export_csv():
        try:
            doc = db.collection('weather_data').document('live').get()
            data = doc.to_dict()
            if not data:
                print("❌ Nicio data de exportat.")
                return
            
            row = {
                'timestamp': data.get('timestamp'),
                'esp32_1': data.get('esp32_1', ''),
                'esp32_2': data.get('esp32_2', ''),
            }
            df = pd.DataFrame([row])
            csv_content = df.to_csv(index=False)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w') as f:
                f.write(csv_content)
                temp_path = f.name

            ui.download(temp_path, filename="export_date.csv")
        except Exception as e:
            print(f"[EXPORT] ❌ {e}")

    ui.button('⬇️ Export date (CSV)', on_click=export_csv, color='primary').classes('rounded-full shadow hover:shadow-lg m-4')

    # === Update date
    def update():
        try:
            doc = db.collection('weather_data').document('live').get()
            data = doc.to_dict()
            if data is None:
                return

            # ESP32_1
            esp32_1 = data.get('esp32_1')
            if esp32_1:
                m_temp = re.search(r"T:\s*([\d.]+)", esp32_1)
                m_hum = re.search(r"H:\s*([\d.]+)", esp32_1)
                m_pres = re.search(r"P:\s*([\d.]+)", esp32_1)
                m_uv = re.search(r"UV:\s*([\d.]+)", esp32_1)
                m_vis = re.search(r"V:\s*([\d.]+)", esp32_1)
                m_ir = re.search(r"IR:\s*([\d.]+)", esp32_1)

                if m_temp:
                    temp_label.text = f"{m_temp.group(1)} °C"
                if m_hum:
                    hum_label.text = f"{m_hum.group(1)} %"
                if m_pres:
                    pres_label.text = f"{m_pres.group(1)} Pa"
                if m_uv:
                    uv_label.text = f"{m_uv.group(1)}"
                if m_vis:
                    light_label.text = f"{m_vis.group(1)} lux"
                if m_ir:
                    ir_label.text = f"{m_ir.group(1)}"

            # ESP32_2
            esp32_2 = data.get('esp32_2')
            if esp32_2:
                m_ws = re.search(r"Wind Speed:\s*([\d.]+)", esp32_2)
                m_wd = re.search(r"Wind Dir:\s*([A-Z]+)", esp32_2)
                m_rv = re.search(r"Rain Vol:\s*([\d.]+)", esp32_2)

                if m_ws:
                    wind_speed_label.text = f"{m_ws.group(1)} km/h"
                if m_wd:
                    wind_dir_label.text = f"{m_wd.group(1)}"
                if m_rv:
                    rain_vol_label.text = f"{m_rv.group(1)} mm"

            ts = data.get('timestamp')
            if ts:
                last_update_label.text = f"Ultima actualizare: {ts.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                last_update_label.text = "Ultima actualizare: ---"

        except Exception as e:
            print(f"[NiceGUI] ❌ {e}")

    ui.timer(600, update)  # 10 minute

    # === Force gradient fundal after Tailwind loaded
    ui.run_javascript(
        'document.body.style.background = "linear-gradient(135deg, #add8e6 0%, #ffffff 100%)";'
    )

    # === Footer
    with ui.row().classes('footer w-full justify-center items-center shadow-inner p-3 mt-4'):
        ui.label('© 2025 Stație Meteo IoT 5G 🚀').classes('text-xs')

# === pornire ===
ui.run()
