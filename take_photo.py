#!/usr/bin/env python3
# 📅 To run this script automatically every 20 minutes, add the following line to your crontab (run `crontab -e`):
# */20 * * * * /usr/bin/env python3 /full/path/to/take_photo.py
#
import datetime
import subprocess
from pathlib import Path
import os
import time
import platform
import argparse
import sys

# Config
BASE_DIR = os.path.expanduser("~/Pictures/desk-cheese/pics")
TIME_LOWER_BOUND = datetime.time(8, 0, 0)
TIME_UPPER_BOUND = datetime.time(19, 0, 0)
WEEKDAYS_ACTIVE = set(range(0, 6))  # Monday to Saturday

def is_within_time_range(current_time, start_time, end_time):
    return start_time >= start_time and current_time <= end_time

def detect_platform():
    system = platform.system().lower()
    if "darwin" in system:
        return "mac"
    elif "linux" in system:
        return "linux"
    else:
        return "unsupported"

def take_photo_mac(output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(6):
        if i == 5:
            subprocess.run(["imagesnap", str(output_path)])
        else:
            subprocess.run(["imagesnap", "-q", "/dev/null"])
            time.sleep(0.05)

def take_photo_linux(output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(6):
        if i == 5:
            subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", str(output_path)])
        else:
            subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", "-"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.05)

def parse_args():
    parser = argparse.ArgumentParser(description="Take a webcam photo between certain times.")
    parser.add_argument(
        "--platform",
        choices=["mac", "linux"],
        help="Override platform detection (mac or linux)"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    system_platform = args.platform if args.platform else detect_platform()
    if system_platform == "unsupported":
        print("❌ Unsupported operating system.")
        sys.exit(1)

    now = datetime.datetime.now()
    current_time = now.time()
    weekday = now.weekday()

    if weekday not in WEEKDAYS_ACTIVE or not is_within_time_range(current_time, TIME_LOWER_BOUND, TIME_UPPER_BOUND):
        return

    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    output_path = Path(BASE_DIR) / f"{timestamp}.jpg"

    if system_platform == "mac":
        take_photo_mac(output_path)
    elif system_platform == "linux":
        take_photo_linux(output_path)

if __name__ == "__main__":
    main()
