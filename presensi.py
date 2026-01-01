#!/usr/bin/env python3
import evdev
from evdev import InputDevice, ecodes
import requests
import logging
import time
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/logs/presensi.log"),
        logging.StreamHandler()
    ]
)

# Gunakan env var jika tersedia, atau default ke URL Anda
BASE_URL = os.getenv("BASE_URL", "https://dev.zeneight.xyz/absensi-be/absensi/siswa")
# Keyword untuk mencari nama device scanner
SCANNER_KEYWORDS = ["USBKey", "Barcode", "Scanner", "HID"]

keymap = {
    2: "1", 3: "2", 4: "3", 5: "4", 6: "5",
    7: "6", 8: "7", 9: "8", 10: "9", 11: "0",
    16: "q", 17: "w", 18: "e", 19: "r",
    20: "t", 21: "y", 22: "u", 23: "i", 24: "o", 25: "p",
    30: "a", 31: "s", 32: "d", 33: "f", 34: "g", 35: "h",
    36: "j", 37: "k", 38: "l",
    44: "z", 45: "x", 46: "c", 47: "v", 48: "b", 49: "n", 50: "m",
}

def find_scanner():
    """Mencari perangkat scanner secara otomatis di /dev/input/"""
    while True:
        try:
            devices = [InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                # Cek apakah nama device mengandung keyword scanner
                if any(key.lower() in device.name.lower() for key in SCANNER_KEYWORDS):
                    logging.info(f"[DEVICE] Scanner ditemukan: {device.name} pada {device.path}")
                    return device
            logging.warning("[DEVICE] Scanner tidak ditemukan. Mencari ulang dalam 5 detik...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"[SYSTEM ERROR] Gagal list devices: {e}")
            time.sleep(5)

def send_presensi(siswa_id):
    url = f"{BASE_URL}/{siswa_id}"
    try:
        # Menambahkan timeout agar script tidak hang jika koneksi internet Orange Pi drop
        r = requests.get(url, timeout=10)
        logging.info(f"[SCAN {siswa_id}] -> {r.status_code} {r.text.strip()}")
    except Exception as e:
        logging.error(f"[API ERROR] {siswa_id} Gagal terkirim: {e}")

def main():
    while True: # Outer loop untuk menjaga script tetap jalan jika scanner terputus
        dev = find_scanner()
        try:
            logging.info(f"Listening on {dev.name} ({dev.path})...")
            
            # Ambil kontrol eksklusif agar input scanner tidak 'nyasar' ke terminal lain
            dev.grab() 
            
            buffer = ""
            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:  # key down
                    keycode = event.code
                    if keycode == 28:  # Enter
                        if buffer:
                            send_presensi(buffer)
                            buffer = ""
                    else:
                        if keycode in keymap:
                            buffer += keymap[keycode]
                            
        except (OSError, Exception) as e:
            logging.error(f"[DEVICE ERROR] Koneksi scanner terputus: {e}")
            try:
                dev.ungrab()
            except:
                pass
            logging.info("Mencoba menyambungkan ulang...")
            time.sleep(2) # Jeda sebelum mencari ulang

if __name__ == "__main__":
    main()
