#!/bin/bash
set -e

INTERFACE="wlan0"

case "$1" in
    pre)
        # Enable monitor mode before capture starts
        ip link set "$INTERFACE" down
        iw dev "$INTERFACE" set type monitor
        ip link set "$INTERFACE" up
        ;;
    post)
        # Restore managed mode after capture stops
        ip link set "$INTERFACE" down
        iw dev "$INTERFACE" set type managed
        ip link set "$INTERFACE" up
        ;;
    *)
        echo "Usage: $0 {pre|post}" >&2
        exit 1
        ;;
esac

exit 0
