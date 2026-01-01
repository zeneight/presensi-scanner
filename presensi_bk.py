#!/usr/bin/env python3
from evdev import InputDevice, ecodes
import requests
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/logs/presensi.log"),
        logging.StreamHandler()
    ]
)

SCANNER_DEVICE = "/dev/input/event0"
BASE_URL = "https://dev.zeneight.xyz/absensi-be/absensi/siswa"

keymap = {
    2: "1", 3: "2", 4: "3", 5: "4", 6: "5",
    7: "6", 8: "7", 9: "8", 10: "9", 11: "0",
    16: "q", 17: "w", 18: "e", 19: "r",
    20: "t", 21: "y", 22: "u", 23: "i", 24: "o", 25: "p",
    30: "a", 31: "s", 32: "d", 33: "f", 34: "g", 35: "h",
    36: "j", 37: "k", 38: "l",
    44: "z", 45: "x", 46: "c", 47: "v", 48: "b", 49: "n", 50: "m",
}

def send_presensi(siswa_id):
    url = f"{BASE_URL}/{siswa_id}"
    try:
        r = requests.get(url, timeout=5)
        logging.info(f"[SCAN {siswa_id}] -> {r.status_code} {r.text}")
    except Exception as e:
        logging.error(f"[API ERROR] {e}")

def main():
    dev = InputDevice(SCANNER_DEVICE)
    logging.info(f"Listening on {SCANNER_DEVICE}...")

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

if __name__ == "__main__":
    main()
