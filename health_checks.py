#!/usr/bin/env python
import os
import shutil
import sys
import socket
import psutil
def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")
def check_disk_full(disk, min_gb, min_percent):
    """Return True if insufficient free space, else return False."""
    du = shutil.disk_usage(disk)
    # Calc % of free space
    precent_free = 100 * du.free / du.total
    # Calc GB of free space
    gigabytes_free = du.free / 2 ** 30
    if gigabytes_free < min_gb or precent_free < min_percent:
        return True
    return False
def check_root_full():
    """Returns True if the root part is full, else returns False."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)
def check_cpu_constrained():
    """Returns True if high CPU usage, else returns False."""
    return psutil.cpu_percent(1) > 75
def check_no_network():
    """Return True if failure to resolve destination, else return False"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True
def main():
    checks=[
        (check_root_full, "Root partition full."),
        (check_cpu_constrained, "High CPU usage."),
        (check_no_network, "Offline.")
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
        if not everything_ok:
            sys.exit(1)   
    print("All Clear!")
    sys.exit(0)
main()