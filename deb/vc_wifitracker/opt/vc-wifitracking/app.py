#!/usr/bin/env python3

import sys
import subprocess
import re
from datetime import datetime


TIMESTAMP_PATTERN = re.compile(r'^(\d+:\d+:\d+)\.\d+')
SIGNAL_PATTERN = re.compile(r'(-\d+)dBm')
BSSID_PATTERN = re.compile(r'BSSID:((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})')
CHANNEL_PATTERN = re.compile(r'CH:\s*(\d+)')
ESSID_PATTERN = re.compile(r'Beacon\s+\((.*?)\)')


def start_tcpdump(interface: str):
    return subprocess.Popen(
        ["tcpdump", "-i", interface, "-e", "-vvv"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )


def format_timestamp(time_str: str) -> str:
    today = datetime.now().date()
    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
    combined = datetime.combine(today, time_obj)
    return combined.strftime("%Y-%m-%d %H:%M:%S")


def parse_line(line: str):
    timestamp_match = TIMESTAMP_PATTERN.search(line)
    signal = SIGNAL_PATTERN.search(line)
    bssid = BSSID_PATTERN.search(line)

    if not (timestamp_match and signal and bssid):
        return None

    channel = CHANNEL_PATTERN.search(line)
    essid = ESSID_PATTERN.search(line)

    formatted_timestamp = format_timestamp(timestamp_match.group(1))

    return (
        formatted_timestamp,
        bssid.group(1).lower(),
        signal.group(1),
        channel.group(1) if channel else "?",
        essid.group(1) if essid else "Hidden",
    )


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <interface>")
        sys.exit(1)

    interface = sys.argv[1]
    process = start_tcpdump(interface)

    for line in process.stdout:
        parsed = parse_line(line)
        if parsed:
            ts, bssid, signal, channel, essid = parsed
            print(f"{ts} | {bssid} | {signal} dBm | CH {channel} | {essid}")


if __name__ == "__main__":
    main()
