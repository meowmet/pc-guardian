# pc-tracker-bot

A Python-based PC tracking and remote control tool using Telegram Bot API.  
Allows you to get system info, webcam photos, screenshots, alarms, and more — all remotely via Telegram commands.

---

## Features

- Get system info: hostname, local/public IP, OS, username  
- Capture and send webcam photo  
- Take screenshots remotely  
- Show popup alarms and warnings on PC  
- Get geolocation info based on IP  
- Multi-command Telegram bot interface  

---

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/pc-tracker-bot.git
   cd pc-tracker-bot
Install dependencies:

bash
Kopyala
Düzenle
pip install -r requirements.txt
Requirements include: requests, opencv-python, pyautogui

Configure your Telegram Bot token and chat ID in config.py or directly in the script.

Run the script:

bash
Kopyala
Düzenle
python pc_tracker_bot.py
Usage
Control your PC remotely by sending commands to your Telegram bot.

Command	Description
/alarm <msg>	Show a popup alarm with beep
/warning <msg>	Show a popup warning (no beep)
/cam	Take and send webcam photo
/specs	Show PC specs
/ip	Show local and public IP addresses
/location	Show geolocation info
/user	Show username
/battery	Take a screenshot and send it
/allinfo	Show full system info and location

Legal Usage
This project is provided “as-is” without any warranty. Use it responsibly and at your own risk.

Permissions
You may use, modify, and distribute this code freely for personal, educational, and non-commercial purposes.

If you use this project commercially or redistribute it, please give proper credit to the original author.

Restrictions
Do not use this project for illegal activities, including unauthorized surveillance or intrusion.

Respect privacy laws and obtain explicit consent from any user before monitoring or collecting data from their device.

Disclaimer
This software is intended for ethical use only. The author is not responsible for any misuse or damage caused by this software.



